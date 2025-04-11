from . import orders, order_details, menu, reviews, customers



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu.router)
    app.include_router(reviews.router)
    app.include_router(customers.router)

