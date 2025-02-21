from user_agents import parse


def detect_device(user_agent: str) -> str:
    ua = parse(user_agent)
    if ua.is_mobile:
        return "phone"
    elif ua.is_tablet:
        return "tablet"
    else:
        return "computer"
