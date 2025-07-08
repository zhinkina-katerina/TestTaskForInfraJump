import logging
from typing import List
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.config import settings
from app.schemas import City

logger = logging.getLogger(__name__)


class LocationGenerator:
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        logger.info("Initializing OpenAI location generator")
        provider = OpenAIProvider(api_key=api_key)
        model = OpenAIModel(model_name, provider=provider)

        self.agent = Agent(
            model=model,
            output_type=List[City],
            system_prompt=(
                "Ти асистент, який шукає цікаві локації в містах. "
                "Повертай лише JSON-список об'єктів у форматі: "
                "[{{'name': '...', 'description': '...', 'coordinates': {{'lat': ..., 'lng': ...}}}}, ...]"
            )
        )
        logger.debug("Agent successfully initialized with model: %s", model_name)

    async def generate(self, city: str, text: str, exclude: List[str], num_places: int) -> List[City]:
        prompt = (
            f"Знайди {num_places} унікальних цікавих локацій у місті {city}. "
            f"Користувач хоче: {text}. "
            f"Не включай: {', '.join(exclude) if exclude else '—'}. "
            f"Поверни JSON-масив об'єктів у форматі: "
            f"[{{'name': '...', 'description': '...', 'coordinates': {{'lat': ..., 'lng': ...}}}}, ...]"
        )

        logger.info("Generating locations for city: %s | text: %s | exclude: %s", city, text, exclude)
        try:
            async with self.agent.iter(prompt) as run:
                async for _ in run:
                    pass
            logger.info("Location generation completed successfully")
            return run.result.output
        except Exception as e:
            logger.error("Error during location generation: %s", str(e))
            raise e


location_generator = LocationGenerator(api_key=settings.OPENAI_API_KEY)
