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


