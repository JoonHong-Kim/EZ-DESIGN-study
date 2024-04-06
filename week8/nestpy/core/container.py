import inspect


class Container:
    def __init__(self):
        self.controllers = []
        self.providers = {}

    def add_controller(self, controller):
        self.controllers.append(controller)

    def add_provider(self, provider):
        # CatsController.__init__ 의 argument 타입의 이름과 동일한 provider가 module에서 등록되지 않은 경우 nestjs와 같은 방식으로 에러가 나야 합니다.
        for controller in self.controllers:
            for _, method in inspect.getmembers(controller, inspect.isfunction):
                if method.__name__ == "__init__":
                    for param in inspect.signature(method).parameters.values():
                        if param.annotation.__name__ == provider.__name__:
                            self.providers[provider.__name__] = provider()
                            return
        raise Exception(f'Error: Can\'t resolve dependencies for "{provider.__name__}"')

    def get_controller(self, controller_type):
        for controller in self.controllers:
            if isinstance(controller, controller_type):
                return controller()
        return None

    def get_provider(self, provider_type):
        return self.providers.get(provider_type.__name__, None)

    def inject_dependencies(self):
        for controller in self.controllers:
            for _, method in inspect.getmembers(controller, inspect.isfunction):
                if method.__name__ == "__init__":
                    for param in inspect.signature(method).parameters.values():
                        if param.annotation.__name__ in self.providers:
                            setattr(
                                controller,
                                param.name,
                                self.providers[param.annotation.__name__],
                            )
