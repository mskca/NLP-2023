import openai

def generate_script(cpf): # Função que utiliza uma requisição para a API do ChatGPT para gerar um roteiro utilizando um CPF e um nome aleatório
    openai.api_key = "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"

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um diretor de cinema especializado em criar roteiros, conhecido por usar números aleatórios para identificar pessoas"},
        {"role": "user", "content": f"Faça o roteiro de um atendimento de suporte ao cliente, onde temos o atendente e o usuário com um nome aleatório cada, durante a conversa, pode ser citado o seguinte mumero de identificação aleatório tanto pelo antendente quanto pelo usuário para identificação: {cpf}, o numero sempre deve ser referido como RG, o nome não pode ser numero, faça a saida formato json, com uma lista de falas representando o dialogo, cada fala deve ser um json com os seguintes atributos: nome, genero (M ou F), tipo (usuario ou atendente), e fala, a saida deve ser apenas o objeto json"}
    ]
    )
    return completion


cpfs = ['11.988.980-8', '12.767.962-5', '14.385.084-2', '32.364.239-1', '18.142.622-5', '46.205.054-3', '14.136.407-5', '44.708.681-9', '23.927.158-0', '27.162.482-6', '38.957.182-9', '38.312.283-1', '25.734.645-4', '23.653.215-7', '44.686.991-0', '38.072.281-1', '46.209.434-0', '29.025.737-2', '13.983.951-3', '44.828.451-0', '50.793.967-0', '16.349.573-7', '22.323.081-9', '16.801.604-7', '49.372.169-1', '47.116.727-7', '38.026.422-5', '47.318.275-0', '12.418.976-3', '13.367.862-3', '40.816.145-0', '32.139.311-9', '48.849.757-7', '34.095.926-5', '23.629.405-2', '24.789.679-2', '29.170.235-1', '28.748.111-6', '49.169.819-7', '25.197.979-9', '35.655.437-5', '11.169.651-3', '31.020.869-5', '23.108.883-8', '35.890.762-7', '10.490.001-5', '20.711.411-0', '13.253.743-6', '28.903.096-1', '11.268.708-8', '31.079.037-2', '41.218.871-5', '39.310.494-1', '20.390.427-8', '42.117.233-2', '27.440.440-0', '15.562.650-4', '10.336.616-7', '15.690.930-3', '34.569.441-7', '39.727.332-0', '33.023.455-9', '27.835.214-5', '41.980.154-6', '23.083.734-7', '50.735.313-4', '44.682.646-7', '30.392.191-2', '23.423.872-0', '35.528.595-2', '36.931.008-1', '14.948.101-9', '14.987.880-1', '28.442.677-5', '27.026.634-3', '22.230.033-4', '15.751.568-0', '29.354.201-6', '46.884.832-0', '28.532.677-6', '29.539.520-5', '16.039.815-0', '30.016.061-6', '30.873.350-2', '38.980.512-9', '24.108.682-6', '31.994.381-1', '49.471.665-4', '35.188.031-8', '35.991.369-6', '39.674.232-4', '27.284.991-1', '19.838.082-3', '44.946.573-1', '25.822.619-5', '19.005.555-8', '24.972.261-6', '33.675.904-6', '49.485.435-2', '33.344.584-3']

for i in range(50, 100):
    file = f"{i}"+".txt"
    completion = generate_script(cpfs[i])
    script = str(completion.choices[0].message["content"])
    with open(file, "w") as file:
        file.write(script)