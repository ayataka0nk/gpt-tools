from pydantic import BaseModel, Field


class PromptMessage(BaseModel):
    role: str = Field(..., example='system')
    content: str = Field(..., example="こんにちは")

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }


class LLMSettings(BaseModel):
    model_type: int = Field(..., example=1)
