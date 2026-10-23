select
    fecha,
    valor as valor_dolar
from {{ source('silver', 'dolar') }}