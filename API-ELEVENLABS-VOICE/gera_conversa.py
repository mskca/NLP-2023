import json
import random
import requests
import time
from elevenlabs import generate
from elevenlabs import set_api_key
from elevenlabs import Voice, VoiceDesign, Gender, Age, Accent, play
from elevenlabs import save

PREV_KEY = None
KEY = None

def setApiKey():
    global PREV_KEY
    global KEY
    api_keys = ["190fe0a8fc6ca4eda2ce48e80480e874", "f1c51bf6ce6e357be93ae840b38656bb", "0ba5af2f6adc72648df17448d28da6d9", "adc792a2ab1e1eb99e6bccd6c6e6b1fe", "1e98154226bcd3ce4edcef5a80a509dc", "6e6ae910a85231552abfdce5be0d19d1", "f968cef590895c5fe2e3ca947ccb2955", "e90d53f7bf8030d78ac3e0fd3af197da", "6d6bce88bb5857003f5916137fd5a70b", "8e59d5ed1ea36c6d56fcb3f8441d2528", "351b6a1f4f73f670d388e15169f81058", "e44d10477fe7b8da0a82bde20214a4f5", "5182022b9b8329469b5a89ab924f4d4b", "2ab5f25d0706c8b24c03861c8a174d41", "54e933e177ab841d290121313348aa5a", "f9905331b2307ef3657474f2cc1c5cc2", "4e0b9d2d448a5c8eb8ef3f838b6c2650", "d52313cfe0927d0812c0366e3904d402", "42fa04bbdbd0aab53b652d9baff7b4f8", "e4d0c34a775895ab49a6dc8ea78a9931", "8a385e38d4882af3ab760fac1b7a1a03"]
    while True:
        KEY = random.choice(api_keys)
        if KEY != PREV_KEY:
            PREV_KEY = KEY
            break

    set_api_key(KEY)



base_path = r'C:\Users\msk\Documents\Projeto-NLP\API-ELEVENLABS-VOICE\roteiros-cpf'

def generate_voice(name, genero):
    if genero == 'M' or genero == 'Masculino' or genero == 'masculino':
        genero = Gender.male
    else:
        genero = Gender.female
    
    age = [Age.young, Age.middle_aged, Age.old]
    age = random.choice(age)

    design = VoiceDesign(
        name=name,
        text="Este será o texto padrão para todas as vozes geradas, com o intuito de chegar em 100 caracteres, espero que nao mude nada na voz.",
        voice_description="Exemplo de voz",
        gender=genero,
        age=age,
        accent=Accent.british,
        accent_strength=1.0,
    )
    voice = Voice.from_design(design)
    
    return voice

def gera_audio(voice, fala, conversaId, falaId):
    mp3 = "fala_"+conversaId+"_"+falaId+".mp3"

    audio = generate(
        text=fala,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    
    save(audio, mp3)

    return 0

def remove_voices():
    base_url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "Accept": "application/json",
        "xi-api-key": f"{KEY}"
    }

    response = requests.get(base_url, headers=headers)

    carrega_json = json.loads(response.text)

    voice_ids = []

    for voice in carrega_json['voices']:
        if voice['category'] == 'generated':
            voice_ids.append(voice['voice_id'])

    for voice_id in voice_ids:
        url = base_url + "/" + voice_id
        response = requests.delete(url, headers=headers)

    time.sleep(2)

    return 0

conversaId = 23

for i in range(23, 50):
    print(f'Iniciando conversa: {conversaId}')

    file_path = f'{base_path}\\{i}.txt'
    try:
        with open(file_path, 'r') as file:
            # Read or process the contents of the file here
            file_contents = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        data = json.loads(file_contents)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    
    nome1 = data['dialogo'][0]['nome']
    nome2 = data['dialogo'][1]['nome']

    setApiKey()

    print('removendo vozes\n')
    remove_voices()

    voice1 = generate_voice(nome1, data['dialogo'][0]['genero'])
    voice2 = generate_voice(nome2, data['dialogo'][1]['genero'])

    falaId = 0

    for fala in data['dialogo']:
        if fala['nome'] == nome1:
            gera_audio(voice1, fala['fala'], str(conversaId), str(falaId))
        else:
            gera_audio(voice2, fala['fala'], str(conversaId), str(falaId))
        
        falaId += 1

    conversaId += 1
    
    print('removendo vozes\n')
    remove_voices()
    print('reiniciando!!')
