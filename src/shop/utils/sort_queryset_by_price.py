def sort_queryset_by_price(queryset, sort_by):
    if sort_by == "price_asc":
        return queryset.order_by("price")
    elif sort_by == "price_desc":
        return queryset.order_by("-price")
    else:
        return queryset
