from .image import LoadImageGetRemark,GetRemarkByImage,LoadImage


NODE_CLASS_MAPPINGS = {
    "ComfyUI-load-image-remark": LoadImageGetRemark,
    "ComfyUI-get-remark-by-image": GetRemarkByImage,
    "ComfyUI-load-image": LoadImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-load-image-remark": "风格提示",
    "ComfyUI-get-remark-by-image": "通过图片获取关键词",
    "ComfyUI-load-image": "加载图片（输出原始图片路径）",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]