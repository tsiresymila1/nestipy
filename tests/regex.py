import re

# Your module content
module_content = """
from config.masonite_orm import masonite_factory
from config.peewee import peewee_mysql_factory
from nestipy.common.decorator.module import Module
from nestipy.core.module import NestipyModule
from nestipy.core.module.provider import ModuleProvider
from nestipy.plugins.config_module.config_module import ConfigModule
from nestipy.plugins.config_module.config_service import ConfigService
from nestipy.plugins.masonite_orm_module.masonite_orm_module import MasoniteOrmModule
from nestipy.plugins.peewee_module.peewee_module import PeeweeModule
from nestipy.plugins.strawberry_module.pubsub import PubSub, STRAWBERRY_PUB_SUB
from nestipy.plugins.strawberry_module.strawberry_module import StrawberryModule, StrawberryOption
from src.auth.auth_module import AuthModule
from src.graphql.graphql_module import GraphqlModule
from src.user.user_module import UserModule


from src.invoice.invoice_module import InvoiceModule
@Module(
    imports=[
        ConfigModule.for_root(),
        PeeweeModule.for_root_async(
            use_factory=peewee_mysql_factory,
            inject=[ConfigService]
        ),
        # BeanieModule.for_root(config="mongodb://user:pass@host:27017"),
        MasoniteOrmModule.for_root_async(
            factory=masonite_factory,
            inject=[ConfigService]
        ),
        UserModule,
        AuthModule,
        GraphqlModule,
        StrawberryModule.for_root(
            imports=[GraphqlModule],
            option=StrawberryOption(graphql_ide='graphiql')
        ),
    ],
    providers=[
        # AppMiddleware,
        ModuleProvider(provide='TEST_PROVIDE', use_value='ProviderTest'),
        ModuleProvider(provide=STRAWBERRY_PUB_SUB, use_value=PubSub())
    ]
)
class AppModule(NestipyModule):

    def on_startup(self):
        pass
"""

# Define the regular expression pattern for capturing all content within @Module
module_pattern = r'@Module\(\s*(.*?)\s*\)\s*class\s+(\w+)\(.*\):'

# Search for @Module decorator in the module content
match = re.search(module_pattern, module_content, re.DOTALL)
if match:
    module_content_within_module = match.group(1).strip()
    print(module_content_within_module)
