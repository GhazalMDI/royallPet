from django import template

register = template.Library()


@register.filter
def check_like(product, user):
    if product.product_like.filter(user_id=user.id).exists():
        return 'fa-solid'
    return 'fa-regular'

@register.filter
def replay(comment):
    if comment := comment.replay_comment.filter(active=True):
        return comment
