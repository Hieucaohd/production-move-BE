class Endpoint:
    HELLO_WORLD = "/"
    LOGIN = "/api/login"
    CREATE_MANUFACTURE_FACTORY = "/api/admins/create-manufacture-factory"
    CREATE_DISTRIBUTION_AGENT = "/api/admins/create-distribution-agent"
    CREATE_WARRANTY_CENTER = "/api/admins/create-warranty-center"
    CREATE_PRODUCT_LINE = "/api/admins/create-production-line"
    CREATE_PRODUCTION_LOT = "/api/manufacture-factories/create-production-lot"
    EXPORT_PRODUCTION_LOT = "/api/manufacture-factories/export-production-lot"
    SOLD_PRODUCTION = "/api/distribution-agents/sold-production"
    GUARANTEE_PRODUCTION = "/api/distribution-agents/guarantee"
    GUARANTEE_DONE = "/api/warranty-center/guarantee-done"
    WARRANTY_SEND_BACK_FACTORY = "/api/warranty-center/send-back-to-factory"

    ALL_PRODUCT_LINES = "/api/product-lines"
    ALL_MANUFACTURE_FACTORIES = "/api/manufacture-factories"
    ALL_DISTRIBUTION_AGENTS = "/api/distribution-agents"
    ALL_WARRANTY_CENTERS = "/api/warranty-centers"
    ALL_PRODUCTIONS = "/api/productions"
    ALL_PRODUCTION_LOTS = "/api/production-lots"
    PRODUCTIONS_ERROR = "/api/manufacture-factories/productions-error"


