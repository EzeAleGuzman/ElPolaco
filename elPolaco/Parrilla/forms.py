# forms.py
from django import forms
from .models import Pedido, DetallePedido, Producto


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["numero", "mesa", "nombre", "total", "pagado", "para_llevar", "nota"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "mesa": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "total": forms.NumberInput(attrs={"class": "form-control"}),
            "pagado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "para_llevar": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "nota": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        # Se pasa el pedido a la vista para saber si ya tiene una mesa asignada
        pedido = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        # Si ya tiene una mesa asignada, deshabilitamos el campo de mesa
        if pedido and pedido.mesa:
            self.fields["mesa"].disabled = True  # Deshabilita el campo de mesa

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")

        return nombre


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ["producto", "cantidad"]

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        empty_label="Lista de productos",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    cantidad = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"})
    )


class PedidoNotaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["nota"]
        widgets = {
            "nota": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
