from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
from datasets import load_dataset

# Cargar dataset
dataset = load_dataset('csv', data_files='data/simplified_texts.csv')

# Dividir en entrenamiento y validación
dataset = dataset['train'].train_test_split(test_size=0.2)
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# Tokenizar datos
def preprocess_function(examples):
    inputs = examples["Texto Original"]
    targets = examples["Texto Simplificado"]

    # Tokenizar las entradas
    model_inputs = tokenizer(inputs, max_length=512, padding=True, truncation=True)

    # Tokenizar las etiquetas (texto objetivo)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=128, padding=True, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Cargar modelo preentrenado
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# Configurar entrenamiento
training_args = TrainingArguments(
    output_dir="./models",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
)

# Entrenar el modelo
trainer.train()