from .schemas import Conversation, ConversationCreate, ConversationUpdate, PromptMessage, ConversationMessage
from . import schemas, models
from .models import ConversationModel, ConversationMessageModel
from sqlalchemy import select
from app.database import Session
from datetime import datetime
from .constants import RoleType
from app import llms


def get_conversations(user_id: int, db: Session) -> list[Conversation]:
    statement = select(ConversationModel).where(
        ConversationModel.user_id == user_id).order_by(ConversationModel.created_at.desc())
    conversations = db.execute(statement).scalars().all()
    return list(map(lambda conversation: Conversation.from_conversation_model(conversation), conversations))


def create_conversation(user_id: int, conversation: ConversationCreate, db: Session):
    conversation_model = ConversationModel(
        user_id=user_id,
        title=conversation.title,
        model_type=conversation.model_type,
    )
    db.add(conversation_model)
    db.commit()
    db.refresh(conversation_model)
    return conversation_model


def update_conversation(conversation_id: int, conversation: ConversationUpdate, db: Session):
    statement = select(ConversationModel).where(
        ConversationModel.conversation_id == conversation_id)
    conversation_model = db.execute(statement).scalar_one()
    conversation_model.title = conversation.title
    db.add(conversation_model)
    db.commit()


def get_conversation(conversation_id: int, db: Session) -> Conversation:
    statement = select(ConversationModel).where(
        ConversationModel.conversation_id == conversation_id)
    conversation_model = db.execute(statement).scalar_one()
    return Conversation.from_conversation_model(conversation_model)


def get_conversation_messages(conversation_id: int, db: Session) -> list[ConversationMessage]:
    statement = select(ConversationMessageModel).where(
        ConversationMessageModel.conversation_id == conversation_id).order_by(
        ConversationMessageModel.created_at.asc())
    message_models = db.execute(statement).scalars().all()
    messages = list(
        map(lambda message: ConversationMessage.from_conversation_message_model(message), message_models))
    return messages


def make_prompt_messages(conversation_id: int, db: Session) -> list[PromptMessage]:
    system_message = get_system_message(conversation_id, db)
    # とりあえず直近6件だけ TODO 用途に応じた過去のプロンプト管理を設計
    conversation_message_statement = select(ConversationMessageModel).where(
        ConversationMessageModel.conversation_id == conversation_id).order_by(
        ConversationMessageModel.created_at.desc()).limit(6)
    conversation_message_models = db.execute(
        conversation_message_statement).scalars().all()
    conversation_messages = list(map(lambda message: ConversationMessage.from_conversation_message_model(
        message), conversation_message_models))  # プロンプトでは古い順に使うから並び反転
    conversation_messages.reverse()

    promptMessages = []
    if (system_message is not None):
        promptMessages.append(system_message.to_prompt_message())

    for conversation_message in conversation_messages:
        promptMessages.append(conversation_message.to_prompt_message())
    print(promptMessages)
    return promptMessages


def get_system_message(conversation_id: int, db: Session) -> schemas.ConversationSystemMessage | None:
    statement = select(models.ConversationSystemMessage).where(
        models.ConversationSystemMessage.conversation_id == conversation_id)
    system_message_model = db.execute(statement).scalar_one_or_none()
    if (system_message_model is not None):
        return schemas.ConversationSystemMessage.from_conversation_system_message_model(
            system_message_model)
    else:
        return None


def create_or_update_conversation_settings(
        conversation_id: int,
        system_message_content: str,
        modelType: llms.LLMModelType,
        db: Session) -> int:
    # conversation 更新
    conversation = db.execute(
        select(ConversationModel).where(
            ConversationModel.conversation_id == conversation_id)
    ).scalar_one_or_none()
    conversation.model_type = modelType.id
    db.add(conversation)

    system_message_model: models.SystemMessageModel | None = db.execute(
        select(models.ConversationSystemMessage).where(
            models.ConversationSystemMessage.conversation_id == conversation_id)
    ).scalar_one_or_none()

    if (system_message_model is not None):
        system_message_model.content = system_message_content
        system_message = system_message_model
    else:
        system_message = models.ConversationSystemMessage(
            conversation_id=conversation_id,
            content=system_message_content,
            created_at=datetime.now()
        )
    db.add(system_message)
    db.commit()
    db.refresh(system_message)
    return system_message.conversation_system_message_id


def post_conversation_message(
        conversation_id: int,
        user_message_content: str,
        db: Session,
        chat_completion_service_factory: llms.ChatCompletionServiceFactory):
    conversation = get_conversation(conversation_id=conversation_id, db=db)
    chat_completion_service = chat_completion_service_factory.create(
        llm_settings=llms.LLMSettings(model_type=conversation.model_type))
    user_message = ConversationMessageModel(
        conversation_id=conversation_id,
        role_type=RoleType.USER.id,
        content=user_message_content,
        created_at=datetime.now()
    )
    db.add(user_message)
    db.commit()

    promptMessages = make_prompt_messages(
        conversation_id=conversation_id, db=db)
    try:
        assistant_message_content = ''
        completion = chat_completion_service.stream(
            promptMessages=promptMessages)

        for word in completion:
            assistant_message_content += word
            yield word
        # TODO 通信時に1単語も帰ってこずにエラーが起きた場合、再試行するようにする
        # 一定回数再試行してダメだった場合は、「どうしようもなかったよエラー」を返すようにする
        # エラーの内容も見る必要がある。例えば合計トークン上限に達してた場合はどうあるべきか？など
        # 1単語以上帰ってきた場合、エラー発生時にそこまでのメッセージを保存するようにする
        assistant_message = ConversationMessageModel(
            conversation_id=conversation_id,
            role_type=RoleType.ASSISTANT.id,
            content=assistant_message_content,
            created_at=datetime.now()
        )
        db.add(assistant_message)
        db.commit()
    except Exception as e:
        # TODO 1単語以上返ってきてるなら、エラー発生時にそこまでのメッセージを保存するようにする
        db.rollback()
        raise e
