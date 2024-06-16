import os
import re
from PIL.ExifTags import TAGS
from PIL import Image, ImageOps, ImageSequence
import folder_paths
import numpy as np
import hashlib
import torch

class LoadImageGetRemark:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("正向提示词","负面提示词")
    FUNCTION = "load_image_get_remark"
    CATEGORY = "TimeCapsuleAI"

    @classmethod
    def load_image_get_remark(cls, image):
        comment = ""
        prompt = ""
        negative_prompt = ""

        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)

        exif_data = img._getexif()
        
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'UserComment':
                    comment = value.decode('utf-8', errors='replace')  # 将bytes转换为str，并使用UTF-8编码
                    if comment.startswith("UNICODE"):
                        comment = comment[len("UNICODE "):]
                    break
        else:
            print(f'没有找到备注信息')

        print(f'comment去nul前:{comment}')
        # 去掉文本nul
        comment = comment.replace('\x00', '')
        print(f'comment去nul后:{comment}')

        # 正则表达式匹配Negativeprompt字段前后的数据 并且删掉Negativeprompt后面换行后的数据
        pattern = re.compile(r'(.*?)Negative prompt:(.*?)(?:\n|$)', re.S)
        
        # 使用正则表达式匹配数据
        match = pattern.search(comment)
        if match:
            print("匹配成功~")
            prompt = match.group(1).strip()
            negative_prompt = match.group(2).strip()
            print("prompt:")
            print(prompt)
            print("\n negative_prompt:")
            print(negative_prompt)
        else:
            print("没有匹配到Negativeprompt~")
            # 定义要匹配的字符串数组
            keywords_to_remove = ["Steps:", "Sampler:", "CFG scale:","Seed:","Size:","Clip skip:","Created Date:","Civitai resources:"]  # 替换成你想要匹配的关键词数组
            
            # 逐行处理文本
            lines = comment.strip().split('\n')
            for i in range(len(lines)):
                line = lines[i]
                for keyword in keywords_to_remove:
                    if keyword in line:
                        lines[i] = ''  # 如果行包含关键词，将该行置为空字符串
                        break

            # 过滤空行并重新构建处理后的文本
            prompt = '\n'.join(line for line in lines if line.strip() != '')

            # 输出处理后的文本
            print("没有匹配到negative_prompt的prompt:")
            print(prompt.strip())

        return (prompt, negative_prompt)

    @classmethod
    def IS_CHANGED(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True

#---------------------------------------------------------#

class GetRemarkByImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
                        "image_path": ("STRING", {"forceInput": True}),
                        "prompt": ("STRING", {"default": "", "placeholder": "prompt", "multiline": True}),
                        "negative": ("STRING", {"default": "", "placeholder": "Negative", "multiline": True}),
                    },
                    "hidden": {
                        "unique_id": "UNIQUE_ID",
                        "extra_pnginfo": "EXTRA_PNGINFO",
                    },
                }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("正向提示词","负面提示词")
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "TimeCapsuleAI"

    @classmethod
    def save_images(self, image_path, unique_id=None, extra_pnginfo=None,prompt=None ,negative=None):
        print(f'接收参数 image_path:{image_path}')
        comment = ""
        prompt = ""
        negative_prompt = ""
        
        img = Image.open(image_path)
        print(f'接收参数 img:{img}')
        exif_data = img._getexif()
        print(f'接收参数 exif_data:{exif_data}')
    
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'UserComment':
                    comment = value.decode('utf-8', errors='replace')  # 将bytes转换为str，并使用UTF-8编码
                    if comment.startswith("UNICODE"):
                        comment = comment[len("UNICODE "):]
                    break
        else:
            print(f'没有找到备注信息')

        print(f'comment去nul前:{comment}')
        # 去掉文本nul
        comment = comment.replace('\x00', '')
        print(f'comment去nul后:{comment}')

        # 正则表达式匹配Negativeprompt字段前后的数据 并且删掉Negativeprompt后面换行后的数据
        pattern = re.compile(r'(.*?)Negative prompt:(.*?)(?:\n|$)', re.S)
        
        # 使用正则表达式匹配数据
        match = pattern.search(comment)
        if match:
            print("匹配成功~")
            prompt = match.group(1).strip()
            negative_prompt = match.group(2).strip()
            print("prompt:")
            print(prompt)
            print("\n negative_prompt:")
            print(negative_prompt)
        else:
            print("没有匹配到Negativeprompt~")
            # 定义要匹配的字符串数组
            keywords_to_remove = ["Steps:", "Sampler:", "CFG scale:","Seed:","Size:","Clip skip:","Created Date:","Civitai resources:"]  # 替换成你想要匹配的关键词数组
            
            # 逐行处理文本
            lines = comment.strip().split('\n')
            for i in range(len(lines)):
                line = lines[i]
                for keyword in keywords_to_remove:
                    if keyword in line:
                        lines[i] = ''  # 如果行包含关键词，将该行置为空字符串
                        break

            # 过滤空行并重新构建处理后的文本
            prompt = '\n'.join(line for line in lines if line.strip() != '')

            # 输出处理后的文本
            print("没有匹配到negative_prompt的prompt:")
            print(prompt.strip())

        a = "不是"
        b = "哥们"
        return {"ui": {"prompt": a, "negative": b}, "result": (prompt,negative_prompt,)}


class LoadImage:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True})
            }
        }

    CATEGORY = "TimeCapsuleAI"
    RETURN_TYPES = ("STRING", "IMAGE", "MASK")
    FUNCTION = "load_image"

    @classmethod
    def load_image(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)
        output_images = []
        output_masks = []

        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        print(f'输出参数 image_path:{image_path}')
        return (image_path, output_image, output_mask)

    @classmethod
    def IS_CHANGED(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True