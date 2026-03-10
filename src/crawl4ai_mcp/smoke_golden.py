from __future__ import annotations

import asyncio

from .config import get_settings
from .crawler import CrawlService, FetchOptions

GOLDEN_URLS = [
    "https://zhuanlan.zhihu.com/p/1947787094299746426",
    "https://www.zhihu.com/people/phppan",
    "https://mp.weixin.qq.com/s/vdI4M1Ly8XTnJ6PqpQcEaA",
    "https://code.claude.com/docs/zh-CN/hooks",
    "https://medium.com/@sampan090611/claude-code-feels-like-a-senior-dev-heres-what-actually-makes-it-different-and-what-the-49c02b456d9c",
    "https://blog.csdn.net/Dontla/article/details/150590085",
]


async def _main() -> None:
    settings = get_settings()
    async with CrawlService(settings) as service:
        for url in GOLDEN_URLS:
            res = await service.fetch(
                url=url,
                options=FetchOptions(format="markdown", max_chars=200_000),
            )
            print("\n===", url)
            title = res.get("title")
            content = str(res.get("content") or "")
            print("title:", title)
            print("format:", res.get("content_format"), "chars:", len(content))
            print(content[:800].replace("\n", "\\n"))


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
