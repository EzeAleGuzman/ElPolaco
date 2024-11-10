from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos')
    stock = models.IntegerField()
    categoria = models.CharField(max_length=50, choices=[
        ('bebida', 'Bebida'),
        ('entrada', 'Entrada'),
        ('plato_principal', 'Plato Principal'),
        ('postre', 'Postre'),
    ])
    
    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    ESTADOS = [
        ('libre', 'Libre'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada')
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='libre')
    
    def __str__(self):
        return (f'Mesa {self.numero} - {self.Estados}')

class Pedido(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)
    
    
    def calcular_total(self):
        self.total = sum(producto.precio for producto in self.productos.all())
        self.save()

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.mesa.numero}'