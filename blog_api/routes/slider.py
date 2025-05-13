from ninja import Router

router = Router(tags=['Slider'])

@router.get('/slider/')
def get_slider_items(request):
    return []
