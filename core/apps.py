from django.apps import AppConfig
import cloudinary

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
cloudinary.config(
    cloud_name="dfkurqnpj",
    api_key="739394649499943",
    api_secret="cSwMjCvq9E_HJuEXhmPyXQ1JiKg"
)