from .models import Autor, Mensaje, Notificacion


def mensajes_no_leidos(request):
    if not request.user.is_authenticated:
        return {
            "total_mensajes_no_leidos": 0,
            "total_notificaciones_no_leidas": 0,
        }

    autor = Autor.objects.filter(usuario=request.user).first()
    if not autor:
        return {
            "total_mensajes_no_leidos": 0,
            "total_notificaciones_no_leidas": 0,
        }

    total_mensajes = Mensaje.objects.filter(
        destinatario=autor,
        visto=False
    ).count()

    total_notificaciones = Notificacion.objects.filter(
        autor=autor,
        leida=False
    ).count()

    return {
        "total_mensajes_no_leidos": total_mensajes,
        "total_notificaciones_no_leidas": total_notificaciones,
    }