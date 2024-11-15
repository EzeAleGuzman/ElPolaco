# forms.py
from django import forms
from .models import Pedido, DetallePedido, Producto

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

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']

    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label="Seleccionar Producto", widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

