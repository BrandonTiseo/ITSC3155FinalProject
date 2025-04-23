from . import customers, menu, order_details, orders, promotion, resources, reviews, recipes



def load_routes(app):
    app.include_router(customers.router)
    app.include_router(menu.router)
    app.include_router(order_details.router)
    app.include_router(orders.router)
    app.include_router(recipes.router)
    app.include_router(promotion.router)
    app.include_router(resources.router)
    app.include_router(reviews.router)

