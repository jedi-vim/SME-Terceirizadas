DROP VIEW IF EXISTS solicitacoes_consolidadas;
CREATE OR REPLACE VIEW solicitacoes_consolidadas AS
-- Essa view consolida todas as solicitacoes

-- alteração de cardápio
-- inclusao de alimentacao normal
-- inclusao de alimentacao continua
-- Inversoes de cardapio
-- Suspensoes de Alimentacao
-- Kit Lanches Solicitacoes Avulsas
-- kit lanche unificado


SELECT cardapio.id,
       cardapio.uuid,
       lote.nome AS lote,
       cardapio.data_inicial AS data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'ALT_CARDAPIO' AS tipo_doc,
       'Alteração de cardápio' AS desc_doc,
       logs.status_evento,
       cardapio.status as status
FROM cardapio_alteracaocardapio AS cardapio,
     escola_escola AS escola,
     escola_diretoriaregional AS dre,
     escola_lote AS lote,
     dados_comuns_logsolicitacoesusuario AS logs
WHERE escola.id = cardapio.escola_id
  AND lote.id = escola.lote_id
  AND dre.id = escola.diretoria_regional_id
  AND cardapio.uuid = logs.uuid_original

GROUP BY cardapio.id,
         lote.nome,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
		 logs.criado_em,
		 logs.status_evento,
         escola.diretoria_regional_id
UNION

SELECT inc_alimentacao.id,
       inc_alimentacao.uuid,
       lote.nome AS lote,
       min(inc_alimentacao_item.data) AS data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'INC_ALIMENTA' AS tipo_doc,
       'Inclusão de alimentação' AS desc_doc,
       logs.status_evento,
       inc_alimentacao.status as status
FROM inclusao_alimentacao_grupoinclusaoalimentacaonormal AS inc_alimentacao,
     escola_escola AS escola,
     escola_lote AS lote,
     escola_diretoriaregional AS dre,
     dados_comuns_logsolicitacoesusuario AS logs,
     inclusao_alimentacao_inclusaoalimentacaonormal as inc_alimentacao_item
WHERE escola.id = inc_alimentacao.escola_id
  AND lote.id = escola.lote_id
  AND dre.id = escola.diretoria_regional_id
  AND inc_alimentacao.uuid = logs.uuid_original
  AND inc_alimentacao_item.grupo_inclusao_id = inc_alimentacao.id
GROUP BY inc_alimentacao.id,
         lote.nome,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
		 logs.criado_em,
		 logs.status_evento,
         escola.diretoria_regional_id

UNION

SELECT inc_alimentacao_continua.id,
       inc_alimentacao_continua.uuid,
       lote.nome AS lote,
       inc_alimentacao_continua.data_inicial AS data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'INC_ALIMENTA_CONTINUA' AS tipo_doc,
       'Inclusão de alimentação contínua' AS desc_doc,
       logs.status_evento,
       inc_alimentacao_continua.status as status
FROM inclusao_alimentacao_inclusaoalimentacaocontinua AS inc_alimentacao_continua,
     escola_escola AS escola,
     escola_lote AS lote,
     escola_diretoriaregional AS dre,
     dados_comuns_logsolicitacoesusuario AS logs
WHERE escola.id = inc_alimentacao_continua.escola_id
  AND lote.id = escola.lote_id
  AND dre.id = escola.diretoria_regional_id
  AND inc_alimentacao_continua.uuid = logs.uuid_original

GROUP BY inc_alimentacao_continua.id,
         lote.nome,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
		 logs.criado_em,
		 logs.status_evento,
         escola.diretoria_regional_id
UNION

SELECT inv_cardapio.id,
       inv_cardapio.uuid,
       lote.nome AS lote,
       CASE WHEN cardapio_de.data <= cardapio_para.data THEN cardapio_de.data ELSE cardapio_para.data END AS data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'INV_CARDAPIO' AS tipo_doc,
       'Inversão de cardápio' AS desc_doc,
       logs.status_evento,
       inv_cardapio.status as status
FROM cardapio_inversaocardapio AS inv_cardapio,
     escola_escola AS escola,
     escola_diretoriaregional AS dre,
     escola_lote AS lote,
     dados_comuns_logsolicitacoesusuario AS logs,
     cardapio_cardapio as cardapio_de,
	 cardapio_cardapio as cardapio_para
WHERE escola.id = inv_cardapio.escola_id
  AND lote.id = escola.lote_id
  AND inv_cardapio.uuid = logs.uuid_original
  AND dre.id = escola.diretoria_regional_id
  AND cardapio_de.id = inv_cardapio.cardapio_de_id
  AND cardapio_para.id = inv_cardapio.cardapio_para_id
GROUP BY inv_cardapio.id,
         lote.nome,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
		 logs.criado_em,
		 logs.status_evento,
         escola.diretoria_regional_id,
         cardapio_de.data,
         cardapio_para.data
UNION

SELECT kit_lanche.id,
       kit_lanche.uuid,
       'lote' AS lote,
       min(kit_lanche_item.data) as data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       'c09c5187-f026-44d5-a0ef-423dbc408cca' as escola_uuid,
       logs.criado_em,
       'KIT_LANCHE_UNIFICADA' AS tipo_doc,
       'Kit lanche unificado' AS desc_doc,
       logs.status_evento,
       kit_lanche.status as status
FROM kit_lanche_solicitacaokitlancheunificada AS kit_lanche,
     escola_diretoriaregional AS dre,
     dados_comuns_logsolicitacoesusuario AS logs,
     kit_lanche_solicitacaokitlanche as kit_lanche_item
WHERE kit_lanche.diretoria_regional_id = dre.id
  AND kit_lanche.uuid = logs.uuid_original
  AND kit_lanche_item.id = kit_lanche.id

GROUP BY kit_lanche.id,
		 dre_uuid,
		 dre_nome,
		 logs.criado_em,
		 logs.status_evento
UNION

SELECT kit_lanche.id,
       kit_lanche.uuid,
       lote.nome AS lote,
       min(kit_lanche_item.data) as data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'KIT_LANCHE_AVULSA' AS tipo_doc,
       'Kit lanche avulso' AS desc_doc,
       logs.status_evento,
       kit_lanche.status as status
FROM kit_lanche_solicitacaokitlancheavulsa AS kit_lanche,
     escola_escola AS escola,
     escola_diretoriaregional AS dre,
     escola_lote AS lote,
     dados_comuns_logsolicitacoesusuario AS logs,
     kit_lanche_solicitacaokitlanche as kit_lanche_item
WHERE escola.id = kit_lanche.escola_id
  AND lote.id = escola.lote_id
  AND kit_lanche.uuid = logs.uuid_original
  AND dre.id = escola.diretoria_regional_id
  AND kit_lanche_item.id = kit_lanche.id

GROUP BY kit_lanche.id,
         lote.nome,
		 logs.criado_em,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
		 logs.status_evento,
         escola.diretoria_regional_id
UNION


SELECT susp_alimentacao.id,
       susp_alimentacao.uuid,
       lote.nome AS lote,
       min(susp_alimentacao_item.data) AS data_doc,
       dre.uuid as dre_uuid,
       dre.nome as dre_nome,
       escola.uuid as escola_uuid,
       logs.criado_em,
       'SUSP_ALIMENTACAO' AS tipo_doc,
       'Suspensão de alimentação' AS desc_doc,
       logs.status_evento,
       susp_alimentacao.status as status
FROM cardapio_gruposuspensaoalimentacao AS susp_alimentacao,
     escola_escola AS escola,
     escola_lote AS lote,
     escola_diretoriaregional AS dre,
     dados_comuns_logsolicitacoesusuario AS logs,
	 cardapio_suspensaoalimentacao as susp_alimentacao_item
WHERE escola.id = susp_alimentacao.escola_id
  AND lote.id = escola.lote_id
  AND susp_alimentacao.uuid = logs.uuid_original
  AND susp_alimentacao_item.grupo_suspensao_id = susp_alimentacao.id
  AND dre.id = escola.diretoria_regional_id

GROUP BY susp_alimentacao.id,
         lote.nome,
		 logs.criado_em,
		 logs.status_evento,
		 escola_uuid,
		 dre_uuid,
		 dre_nome,
         escola.diretoria_regional_id
ORDER BY criado_em DESC
