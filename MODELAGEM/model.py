import spacy
from spacy.training.example import Example, offsets_to_biluo_tags
import jsonlines
from sklearn.model_selection import train_test_split

# Substitua 'pt_core_news_sm' pelo modelo spaCy adequado para o seu idioma.
nlp = spacy.blank("pt")

# Se você já tiver um modelo pré-treinado e quiser aprimorá-lo, você pode carregá-lo usando:
# nlp = spacy.load("seu_modelo")

# Caminho para o arquivo JSONL de treinamento
file_path = 'C:\\Users\\msk\\Documents\\Projeto-NLP\\MODELAGEM\\corpusv1.jsonl'

# Convertendo os dados para o formato aceito pelo spaCy com tags BILUO alinhadas
examples = []
with jsonlines.open(file_path) as reader:
    for line in reader:
        text = line["text"]
        entities = line["label"]
        tags = offsets_to_biluo_tags(nlp.make_doc(text), entities)
        example = Example.from_dict(nlp.make_doc(text), {"entities": tags})
        examples.append(example)

# Dividindo o conjunto de dados em treinamento (80%) e teste (20%)
train_data, test_data = train_test_split(examples, test_size=0.2, random_state=42)

# Adicionando o pipeline NER e rótulos
ner = nlp.add_pipe("ner")
ner.add_label("NOME")
ner.add_label("NUMERO")

# Configurações de treinamento
n_iter = 10
optimizer = nlp.begin_training()

# Inicializando contadores para métricas por entidade
entity_metrics = {label: {"precision": 0, "recall": 0, "f1": 0} for label in ["NOME", "NUMERO"]}
total_metrics = {"precision": 0, "recall": 0, "f1": 0}

# Treinando o modelo por várias iterações
for itn in range(n_iter):
    losses = {}
    for example in train_data:
        nlp.update([example], drop=0.5, losses=losses)
    
    # Avaliando o modelo no conjunto de teste a cada iteração
    with nlp.select_pipes(enable=["ner"]):
        scores = nlp.evaluate(test_data)
        total_metrics["precision"] += scores.get("ents_p", 0)
        total_metrics["recall"] += scores.get("ents_r", 0)
        total_metrics["f1"] += scores.get("ents_f", 0)
        
        for label in ["NOME", "NUMERO"]:
            entity_metrics[label]["precision"] += scores['ents_per_type'][label]['p']
            entity_metrics[label]["recall"] += scores['ents_per_type'][label]['r']
            entity_metrics[label]["f1"] += scores['ents_per_type'][label]['f']
    
    print(f"Iteração {itn+1}: Losses - {losses}")

# Calculando médias das métricas por entidade
for label in ["NOME", "NUMERO"]:
    entity_metrics[label]["precision"] /= n_iter
    entity_metrics[label]["recall"] /= n_iter
    entity_metrics[label]["f1"] /= n_iter

# Calculando médias das métricas gerais
total_metrics["precision"] /= n_iter
total_metrics["recall"] /= n_iter
total_metrics["f1"] /= n_iter

# Imprimindo métricas por entidade
for label in ["NOME", "NUMERO"]:
    print(f"\nMetrics for Entity '{label}':")
    print(f"{label} Precision: {entity_metrics[label]['precision']:.3%}")
    print(f"{label} Recall: {entity_metrics[label]['recall']:.3%}")
    print(f"{label} F1 Score: {entity_metrics[label]['f1']:.3%}")

# Imprimindo métricas gerais
print("\nMetrics Overall:")
print(f"Precision: {total_metrics['precision']:.3%}")
print(f"Recall: {total_metrics['recall']:.3%}")
print(f"F1 Score: {total_metrics['f1']:.3%}")
