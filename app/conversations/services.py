from .schemas import Conversation, ConversationCreate, ConversationUpdate, PromptMessage, ConversationMessage
from .models import ConversationModel, ConversationMessageModel
from sqlalchemy import select
from app.database import Session
from datetime import datetime
from .constants import RoleType
from app.llms import ChatCompletion


def get_conversations(user_id: int, db: Session) -> list[Conversation]:
    statement = select(ConversationModel).where(
        ConversationModel.user_id == user_id).order_by(ConversationModel.created_at.desc())
    conversations = db.execute(statement).scalars().all()
    return list(map(lambda conversation: Conversation.from_conversation_model(conversation), conversations))


def create_conversation(user_id: int, conversation: ConversationCreate, db: Session):
    conversation_model = ConversationModel(
        user_id=user_id,
        title=conversation.title)
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


def get_conversation_messages(conversation_id: int, db: Session) -> list[ConversationMessage]:
    statement = select(ConversationMessageModel).where(
        ConversationMessageModel.conversation_id == conversation_id).order_by(
        ConversationMessageModel.created_at.asc())
    message_models = db.execute(statement).scalars().all()
    messages = list(
        map(lambda message: ConversationMessage.from_conversation_message_model(message), message_models))
    return messages


def make_prompt_messages(conversation_id: int, db: Session) -> list[PromptMessage]:
    # とりあえず直近6件だけ TODO 用途に応じた過去のプロンプト管理を設計
    statement = select(ConversationMessageModel).where(
        ConversationMessageModel.conversation_id == conversation_id).order_by(
        ConversationMessageModel.created_at.desc()).limit(6)
    conversation_message_models = db.execute(statement).scalars().all()
    conversation_messages = list(map(lambda message: ConversationMessage.from_conversation_message_model(
        message), conversation_message_models))  # プロンプトでは古い順に使うから並び反転
    conversation_messages.reverse()
    promptMessages = []
    promptMessages.append(PromptMessage(
        role=RoleType.SYSTEM.role,
        content="涼宮ハルヒの憂鬱に登場する、涼宮ハルヒになりきって会話してください。"
    ))
    for conversation_message in conversation_messages:
        promptMessages.append(conversation_message.to_prompt_message())
    return promptMessages


def store_system_message(conversation_id: int, system_message_content: str, db: Session):
    system_message = ConversationMessageModel(
        conversation_id=conversation_id,
        role_type=RoleType.SYSTEM.id,
        content=system_message_content,
        created_at=datetime.now()
    )
    db.add(system_message)
    db.commit()


def post_conversation_message(
        conversation_id: int,
        user_message_content: str,
        db: Session,
        chatCompletion: ChatCompletion):
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
        completion = chatCompletion.stream(promptMessages=promptMessages)

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
