from django.db import models
from django.urls import reverse


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="productos")
    categoria = models.CharField(
        max_length=50,
        choices=[
            ("sandwiches", "Sandwiches"),
            ("porciones", "Porciones"),
            ("ensaladas", "Ensaladas"),
            ("papas", "Papas"),
            ("bebidas", "Bebidas"),
        ],
    )

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    mesa = models.ForeignKey("Mesa", on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)
    para_llevar = models.BooleanField(default=False)

    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detallepedido_set.all())
        self.total = total
        self.save()

    def save(self, *args, **kwargs):

        if self.mesa:
            if not self.pagado and self.mesa.estado != "ocupada":
                self.mesa.estado = "ocupada"
                self.mesa.save()

            elif self.pagado and self.mesa.estado != "libre":
                self.mesa.estado = "libre"
                self.mesa.save()

        super().save(*args, **kwargs)

    def __str__(self):
        fecha_formateada = self.fecha.strftime("%d/%m/%Y %H:%M")
        return f'Pedido {self.id} - Mesa {self.mesa.numero if self.mesa else "Sin mesa"} - {fecha_formateada} - {self.nombre} - {self.total}'

    def get_absolute_url(self):
        return reverse("detalle_pedido", kwargs={"pedido_id": self.pk})


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_subtotal(self):
        self.subtotal = self.producto.precio * self.cantidad

    def save(self, *args, **kwargs):
        # Calcular el subtotal antes de guardar
        self.calcular_subtotal()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id} -Pedido {self.pedido.nombre} - {self.producto.nombre} - {self.cantidad} x {self.producto.precio} = {self.subtotal}"


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    ESTADOS = [("libre", "Libre"), ("ocupada", "Ocupada"), ("reservada", "Reservada")]
    estado = models.CharField(max_length=10, choices=ESTADOS, default="libre")

    def __str__(self):
        return f"Mesa {self.numero} - {self.estado}"
