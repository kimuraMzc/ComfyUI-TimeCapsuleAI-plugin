from .image import LoadImageGetRemark,GetRemarkByImage,LoadImage


NODE_CLASS_MAPPINGS = {
    "ComfyUI-load-image-remark": LoadImageGetRemark,
    "ComfyUI-get-remark-by-image": GetRemarkByImage,
    "ComfyUI-load-image": LoadImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-load-image-remark": "加载图片获取关键词",
    "ComfyUI-get-remark-by-image": "通过图片获取关键词",
    "ComfyUI-load-image": "加载图片（输出原始图片）",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]