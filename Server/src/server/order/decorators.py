from django.contrib.auth.decorators import user_passes_test, login_required

customer_required = user_passes_test(lambda u: u.isCustomer,
                                     login_url='/authentication/login')


performer_required = user_passes_test(lambda u: u.isPerformer,
                                      login_url='/authentication/login')


def customer_required_dec(view_func):
    decorated_view_func = login_required(customer_required(view_func))
    return decorated_view_func

def performer_required_dec(view_func):
    decorated_view_func = login_required(performer_required(view_func))
    return decorated_view_func
