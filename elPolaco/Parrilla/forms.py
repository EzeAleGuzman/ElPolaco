# forms.py
from django import forms
from .models import Pedido, Mesa

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa', 'nombre', 'total', 'pagado', 'para_llevar']
        widgets = {
            'mesa': forms.Select(),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'pagado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'para_llevar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Filtrar las mesas disponibles (solo las que están libres)
    mesa = forms.ModelChoiceField(queryset=Mesa.objects.filter(estado='libre'), empty_label="Seleccionar mesa")
