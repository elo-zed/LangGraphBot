import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# Load the model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    #attn_implementation="flash_attention_2",
)
txt = "在2026年3月9日，美国佛罗里达州多拉尔的“美洲盾牌”峰会上，美国总统特朗普与来自阿根廷、玻利维亚、特立尼达和多巴哥、以及多米尼加共和国等多国领导人会面，但墨西哥总统谢因鲍姆和古巴领导人未出席。特朗普在峰会期间强调了西半球安全和打击毒品贩运的重要性，随后计划飞往特拉华州多佛，参加六名在伊朗冲突中阵亡美军的尊严转运仪式。峰会的核心目标是加强美洲国家合作、削弱中国在拉美的影响力，并推动地区领导人对安全与经济事务的统一行动。"
# Generate speech with specific instructions
for name,s in [("Aiden","男"),("Serena","女"),("Ono_Anna","女"),("Ryan","男")]:
    wavs, sr = model.generate_custom_voice(
        text=txt,
        language="Chinese", 
        speaker=name,
        instruct=f"充满青春气息,富有节奏,温暖柔和的{s}声", 
    )

    # Save the generated audio
    sf.write(f"{name}.wav", wavs[0], sr)