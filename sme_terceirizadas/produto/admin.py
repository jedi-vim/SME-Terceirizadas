from django.contrib import admin

from .models import (
    Fabricante,
    HomologacaoDoProduto,
    ImagemDoProduto,
    InformacaoNutricional,
    InformacoesNutricionaisDoProduto,
    Marca,
    Produto,
    ProtocoloDeDietaEspecial,
    ReclamacaoDeProduto,
    RespostaAnaliseSensorial,
    SolicitacaoCadastroProdutoDieta,
    TipoDeInformacaoNutricional
)

admin.site.register(Fabricante)
admin.site.register(InformacaoNutricional)
admin.site.register(Marca)
admin.site.register(ProtocoloDeDietaEspecial)
admin.site.register(ReclamacaoDeProduto)
admin.site.register(RespostaAnaliseSensorial)
admin.site.register(TipoDeInformacaoNutricional)
admin.site.register(HomologacaoDoProduto)
admin.site.register(SolicitacaoCadastroProdutoDieta)


class InformacoesNutricionaisDoProdutoInline(admin.TabularInline):
    model = InformacoesNutricionaisDoProduto
    extra = 1


class ImagemDoProdutoInline(admin.TabularInline):
    model = ImagemDoProduto
    extra = 1


@admin.register(Produto)
class ProdutoModelAdmin(admin.ModelAdmin):
    inlines = [InformacoesNutricionaisDoProdutoInline, ImagemDoProdutoInline]
