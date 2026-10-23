select
    fecha,
    valor as valor_uf
from {{ source('silver', 'uf') }}