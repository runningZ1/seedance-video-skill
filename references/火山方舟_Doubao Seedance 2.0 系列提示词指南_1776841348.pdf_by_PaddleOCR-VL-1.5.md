## Doubao Seedance 2.0 系列 提示词指南

火山方舟

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a9c8cdf8-e5aa-4e3a-b00e-6b081476d0b6/markdown_0/imgs/img_in_image_box_11_537_1185_1601.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2Fac1544bbc819fe6ae43aad8e494b622816ab08b13798667e0ee6cefc522a41c7" alt="Image" width="98%" /></div>


### 法律声明

本《火山方舟》的所有内容，包括但不限于文字、商标、架构、图示、图片、页面布局等，其知识产权（著作权、商标权、专利权、商业秘密等）归属于北京火山引擎科技有限公司及其关联公司（火山引擎），非经火山引擎书面同意，任何个人和组织不得复制、使用、修改、转发或以任何违反本《火山方舟》所承载的目的进行传播。

本《火山方舟》陈述内容仅作为产品的通用性介绍和参考性指引，火山引擎保留按“现状”和“当前可用”的形式提供产品和服务的权利。火山引擎不对本《火山方舟》中所载的产品功能、性质、质量、标准等内容进行明示或默示的保证和承诺，最终以您与火山引擎实际签署的协议为准。

如您发现本《火山方舟》有任何错误或歧义，或发现有对本《火山方舟》、产品本身的侵权行为，请与火山引擎取得联系。

联系方式：service@volcengine.com，400-850-0030（周一至周五 10:00-18:00）

## 目录

法律声明___1    
目录___1    
1. Doubao Seedance 2.0 系列提示词指南___1

## 1. Doubao Seedance 2.0 系列提示词指南

Doubao Seedance 2.0 系列（下文简称 Seedance 2.0 系列）模型原生支持音频与视频联合生成，拥有卓越的语义理解与多模态交互能力。本文介绍 Seedance 2.0 系列模型的提示词使用方法和相关技巧，帮助您更高效地利用该模型生成符合需求的优质视频作品。

注意

本指南中呈现的所有视觉（图片、视频）及音频素材，均由 Seedance/Seedream 系列视觉生成模型自主生成。

## 01 总体要领

### 1.1 文本指令的基础公式

Seedance 2.0 系列模型能深度遵循自然语言逻辑，因此您可以根据需求灵活组合以下元素。

必需
主体
运动
这是指令的逻辑基石，用于明确谁正在进行什么动作。

非必需
环境
美学
描述空间背景、光影细节或特定视觉风格，定义画面的整体格调。

非必需
运镜
音频
使用镜头调度或氛围声效等进阶指令，实现视听高度协同的沉浸式产出。

### 1.2 多模态参考的指代控制

除了文字描述，您还可以通过“投喂素材”来锁定画面的理想标准态。Seedance 2.0 系列模型支持图像、音频和视频的深度参考。

明确指代
在提示词中清晰指定参考对象，例如“画面参考 图片1 的构图”或“动作参考 视频2”。

精准迁移
模型将自动提取参考对象中的核心特征，并结合您的文本描述进行创作，确保生成结果在保持创意的同时，具备极高的确定性与还原度。

## 02 文字生成

Seedance 2.0 系列模型支持在 T2V（文生视频）、I2V（图生视频）、R2V（参考生视频）、V2V（视频生视频）等场景下生成常用文字。

模型能根据情境自动匹配合适的风格与颜色，也支持在提示词中指定文字的颜色、风格、出现方式、出现时机、出现位置。

编写时请优先使用常用字，避免生僻字与特殊符号，以确保最佳呈现效果。

### 2.1 广告语 (Slogan)

提示词参考模板：

Plain

「文字内容」+「出现时机」+「出现位置」+「出现方式」，「文字特征（颜色、风格）」

说明

Seedance2.0 能根据情境匹配合适的文字风格，如果对文字表现效果的要求较为严格，可参考本文中的 3.2 多图参考 > Logo 参考。

参考案例：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//b51d4998-2d1f-4fbc-8ba4-bfe489bb020c/markdown_0/imgs/img_in_image_box_110_143_1013_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2Fbfb7efcefe576668642c4712b2002f3bd0e76ed233c2a979df120cd14986c91c" alt="Image" width="75%" /></div>


##### [提示词]

手绘漫画风格，三个人围坐在一起吃图片1中的炸鸡，气氛友好愉悦，后画面逐渐模糊，画面中部显示文字“快乐尽在 Seedance”。

[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//1a79271a-8fcb-4471-b837-cdfd101419a9/markdown_0/imgs/img_in_image_box_110_168_1006_1066.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F48864a4835c71304a92b610bdbd9ea53d7d3c9f0ae5c6d469aaaa4b65bb3b36f" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


### 2.2 字幕

提示词参考模板：

Plain

画面底部出现字幕，字幕内容为“……”，字幕需与音频节奏完全同步。

参考案例：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a0563fa6-fc39-448a-877c-8b1f7a64eb80/markdown_0/imgs/img_in_image_box_112_144_1013_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2Fe4b105f6dca672a7f99d81cdb77e89e3733a793f858738d27cb77edbdc67e319" alt="Image" width="75%" /></div>


##### [參考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a0563fa6-fc39-448a-877c-8b1f7a64eb80/markdown_0/imgs/img_in_image_box_111_719_1007_1221.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2Faf9628bd5c39b74457475915ee4872ccb50042ec661671a8d4f0137b48d8fdf2" alt="Image" width="75%" /></div>


##### [提示词]

生成带有画外音的视频。一个深沉、平静的男声说：“在宏大的宇宙中，我们的世界不过是一个短暂的瞬间。然而，在其中，生命不顾一切地繁荣。”场景应从夜晚缓慢过渡到黎明，星星逐渐消失，太阳从山后升起。画面底部按照台词出现字幕。

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f0b78dec-9200-414f-8165-c190def87f4f/markdown_0/imgs/img_in_image_box_112_144_1013_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2Fa02d04b37966b6dda33e2ab7f2f047ef4a9f85db5bd99d289b4d5b3d52c51053" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">[参考素材]</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f0b78dec-9200-414f-8165-c190def87f4f/markdown_0/imgs/img_in_image_box_110_717_1008_1221.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2Ff48fc5c2a70bf7b6d265efcf1390074cef5812375a49fcf0a19c0ad573cd77f8" alt="Image" width="75%" /></div>


[提示词]

图片中的两人在办公室聊天，女性先说话，她说道：“你每次卡点到，是不是很享受这种刚刚好的感觉？”男性笑着回应：“我有我的节奏”角色说话时，对话随意自然，画面底部出现对应台词字幕。

### 2.3 气泡台词

提示词参考模板：

Plain

「角色」说：“……”，角色话说时周围出现气泡，气泡里写着台词。

参考案例：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//65ae0c64-2615-4c7e-b9af-2f38f2055312/markdown_0/imgs/img_in_image_box_110_369_1014_878.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F259fc7f7068348061046b8aa743fc6e74d7c7b733496e91053625f1e5aed4b7d" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//65ae0c64-2615-4c7e-b9af-2f38f2055312/markdown_0/imgs/img_in_image_box_219_964_967_1385.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fa23c4f28b74a15c66f187ed82b7634bee1a271a5c2ed4ed4fced550ab6c11ece" alt="Image" width="62%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


##### [提示词]

图片1 中的两人穿着运动服在学校的操场跑步，女孩看向男孩，自信地笑着说：“We can definitely do it!

”镜头切到男孩的近景，他犹豫地回答：“Are you sure？”镜头切回女孩的中近景，她语气轻快地说：“Yes！”情绪明亮而坚定。说话的角色周边出现气泡，气泡里是对应台词。

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e233bbc2-9669-4987-bd30-fc0ae55cfc68/markdown_0/imgs/img_in_image_box_111_266_1015_773.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fb63194f4b27124e65ed8c4c3c1eefdf9ec27f76c473bf641cc3b4df007920338" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e233bbc2-9669-4987-bd30-fc0ae55cfc68/markdown_0/imgs/img_in_image_box_149_879_1044_1288.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Ff983e229b99a8d26a742bb6d77961faef111c62a8a1c58ce10c6ed26d8d86892" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


##### [提示词]

参考 图片1 、 图片2 中的女孩形象，女孩在一个草莓园里，摘下一颗，吃了一口，笑着说：“This is the real deal!”女孩周围出现一个气泡，气泡里面写着台词。

## 03 图片参考

Seedance 2.0 系列模型既支持主体多视角参考，也支持场景图、分镜图等多图参考。

使用过程中，如对图片顺序有要求，应按顺序上传，提示词中可使用图片1、图片2……图片n 进行准确指代。

### 3.1 主体多视角图参考

提示词参考模板：

Plain

参考/提取/结合+「图片 n」中的「主体」，生成「画面描述」，保持「主体」特征一致。

指代清楚参考对象即可，模型能够响应的指令包括但不限于以下示例。

商品：

3C数码

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//95fbe5d2-19d4-4537-883d-dc9cf2622ab0/markdown_0/imgs/img_in_image_box_110_703_1016_1213.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2Feb3a0e5ed000c63c851f159ae96225faad10333ca779c01478d81dc7af926aaa" alt="Image" width="76%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//db8ab2a7-a29f-4869-b898-149aaa5b067e/markdown_0/imgs/img_in_image_box_147_145_433_442.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F0fd944d772ff759ca6451ae826773751df12ab4590a246c541fdb5bfb47d0fba" alt="Image" width="24%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//db8ab2a7-a29f-4869-b898-149aaa5b067e/markdown_0/imgs/img_in_image_box_451_145_738_432.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F68820d755910b3fae656519bd153ed4b8ac2475c7a611d49c4669b658089021e" alt="Image" width="24%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//db8ab2a7-a29f-4869-b898-149aaa5b067e/markdown_0/imgs/img_in_image_box_758_145_1045_431.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F63ee4d73ba774c739c23305a1c40fe594c96851edd870039d0f282e5c6a86ddd" alt="Image" width="24%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片3</div> </div>


##### [提示词]

提取 图片1 、 图片2 、 图片3 的相机，把背景换成白色，相机在一个白色桌子上，镜头以特写的形式聚焦相机，然后以相机为主体缓慢旋转，清晰展示相机的正面侧面以及背面。

##### 家居物品

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//db8ab2a7-a29f-4869-b898-149aaa5b067e/markdown_0/imgs/img_in_image_box_111_753_1015_1263.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fe6bfac7385451099c2d940419373f7acb0708c1b32665b4bf3e8dfb8304fefba" alt="Image" width="75%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//d99a2f35-cd97-4fec-b4ee-2d1c5187c654/markdown_0/imgs/img_in_image_box_292_143_581_429.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Ff5b07675d81f519b4b7628979988c237e172d09b1f96bbab6f3b011a55ed3d0a" alt="Image" width="24%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//d99a2f35-cd97-4fec-b4ee-2d1c5187c654/markdown_0/imgs/img_in_image_box_611_145_897_430.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fc348b0b5ea3e70ab625ed8b67bf2504252596865b160cd3914baeafafcb0c878" alt="Image" width="24%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


##### [提示词]

背景为暖调居家场景，中景呈现参考图中的保温杯，镜头平稳推近至保温杯近景，镜头外一只手自然入镜轻握杯身拿起保温杯，镜头跟拍手部微微旋转动作展示。

##### 角色：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//d99a2f35-cd97-4fec-b4ee-2d1c5187c654/markdown_0/imgs/img_in_image_box_110_753_1016_1262.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fcf52316ec1ad7c009f2a74cf9be33bdad6989b9e358791ac765c4ca1a73062ba" alt="Image" width="76%" /></div>


##### [提示词]

参考 图片1 、 图片2 、 图片3 中的女子形象，生成她在一家咖啡店吃蛋糕的画面。

##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//47fb8f44-d5c7-4833-a048-3e0959906096/markdown_0/imgs/img_in_image_box_111_173_1077_745.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F8d32d3a5779e73fc78eec335bf5b59c067aca7a12976868cb687e1b6ce37dd3a" alt="Image" width="81%" /></div>


▲图片1

▲图片2

▲图片3

### 3.2 多图参考

提示词参考模板：

Plain

参考/提取/结合/按照/生成+「图片n」中的「被参考元素描述」，生成「画面描述」，保持「被参考元素」特征一致。

参考案例：

Logo参考

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//53c2333a-ee0e-4bfb-a2ae-c146849d1074/markdown_0/imgs/img_in_image_box_111_143_1014_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2Fbc19760c3cb589a55fe9808c22d072bb6cbb96efb79e106a931cb4a1c6f1dd9a" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//53c2333a-ee0e-4bfb-a2ae-c146849d1074/markdown_0/imgs/img_in_image_box_161_739_701_1142.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2F156cc6b538999449ab24f1d4239667e5421576ca461f8b664373cb037fca3c78" alt="Image" width="45%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//53c2333a-ee0e-4bfb-a2ae-c146849d1074/markdown_0/imgs/img_in_image_box_726_740_1029_1142.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2F8a3638d8a9e110c47eb7e7ac425df04da52e714ac118187667e33cd60f48c780" alt="Image" width="25%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


##### [提示词]

背景是霓虹闪烁的未来都市空中廊道，飞行器与全息广告交织，参考图片2中的女孩，先用中景展示女孩放飞带有全息投影的银色悬浮灯，再镜头拉远展现漫天悬浮灯，画面逐渐模糊，后出现图片1的Logo，整体风格为3D赛博朋克科幻动画风格。

##### 多主体参考

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e4c665c7-f535-42c9-9193-bf80ee13e188/markdown_0/imgs/img_in_image_box_110_143_1014_653.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2Fe0d751be0b7d46518561fa60f6d0d8cb5e1d4061ffd638c78123815b9c91acbf" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e4c665c7-f535-42c9-9193-bf80ee13e188/markdown_0/imgs/img_in_image_box_110_741_590_1141.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F2039eaf053e56c53926f80da4c8453f636e026bbb11031af436c053e9127bff3" alt="Image" width="40%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e4c665c7-f535-42c9-9193-bf80ee13e188/markdown_0/imgs/img_in_image_box_600_742_1078_1141.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F708d3c39a6f3bdd26291b954a57996d264967c7abca8af809a5d0c06ea497a98" alt="Image" width="40%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 图片 2</div> </div>


##### [提示词]

参考图片中的猫猫和狗狗，在一个温馨的公寓里，狗狗在趴着吃狗粮，猫猫走过来，伸出爪子碰了碰狗狗，狗狗看到猫猫后停下吃饭，猫猫依偎在狗狗身边。画面采用暖色调。

##### 多元素参考

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_111_144_1014_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2Fdb724b12f86006f9abbc0b2aa003bdee56f78f31354b1315570b972018596ea3" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_115_699_269_867.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F8ed5250f5bb94dc793b4931c707d0b2bcbf2d0d711bb807f099af36822fcc3a9" alt="Image" width="12%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_281_701_444_865.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F4d2a4c8a0674eb5808e7c22fa11c4be0ab948abfe9f8e8921d8dfbcfb51d9086" alt="Image" width="13%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_478_701_586_866.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fa4df4a5c0c43c2e04d8104bcd1ad1bb9c142bc4814b8abfa268edff8c86da378" alt="Image" width="9%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片3</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_617_699_786_865.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F63cb82e42d325e3cd0281165fdc56fafa6276f074924ad983baa0d9f379fdba2" alt="Image" width="14%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片4</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//adb959d3-94ec-4ac2-855e-6180977b7132/markdown_0/imgs/img_in_image_box_818_708_1052_853.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fb07216401166cedb2931a11a9450ee2f720f624c54e9f7f2b7c40a4968c26dcf" alt="Image" width="19%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 图片 5</div> </div>


##### [提示词]

场景设定在图片4中的餐厅内，店内人来人往。图片1里的女孩身着图片2中的服装，正在整理柜台上的物品。图片3中的男孩是一位顾客，他走上前，想要向女孩索要联系方式。图片5中的标识始终显示在画面的右下角。

##### 多宫格分镜图参考

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2cb1df9e-fa2a-4ee0-8a5d-0a1566a38393/markdown_0/imgs/img_in_image_box_112_142_1013_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A20Z%2F-1%2F%2F2d1c803978dc8eddb9672c419737a0d763773494348c55bad8514507f056a27a" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">[参考素材]</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//05eb1bbb-c155-4d76-b3b6-5f647e088a23/markdown_0/imgs/img_in_image_box_108_173_552_607.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A21Z%2F-1%2F%2F970d44f7b42e4601748dbf436916f0e3cc28d0375ba5f0c8b31c87b46f305e41" alt="Image" width="37%" /></div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//05eb1bbb-c155-4d76-b3b6-5f647e088a23/markdown_0/imgs/img_in_image_box_574_176_1007_609.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A21Z%2F-1%2F%2F97a59f924b542cc728d45d866314acedda64945e02bd0a6712cd6f6baa38477f" alt="Image" width="36%" /></div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//05eb1bbb-c155-4d76-b3b6-5f647e088a23/markdown_0/imgs/img_in_image_box_110_628_552_1066.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A21Z%2F-1%2F%2F2b74f6a68bdcbb97c0041283980b669069568b713d112332fdba0a260eea1de6" alt="Image" width="37%" /></div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//05eb1bbb-c155-4d76-b3b6-5f647e088a23/markdown_0/imgs/img_in_image_box_567_632_1009_1066.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A21Z%2F-1%2F%2F406e3e8b6bf4dc020347ceee18837be246eb9c4cbd9783be260d2b852d58c998" alt="Image" width="37%" /></div>


[提示词]

参考图片中的分镜图，生成打斗激烈的打斗场面。图片中的各个分镜构图要按照顺序出现，之后二人激烈打斗。

分镜图参考

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a5d6d034-52df-4463-835c-491f6ea1a19e/markdown_0/imgs/img_in_image_box_112_142_1013_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F484d945bbc1234da7e90620869c348ecd65ffb77ff2b9ebe2281549b1007f0cc" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//79c4fa05-bd5e-4cb8-bb43-0bdf78f7d216/markdown_0/imgs/img_in_image_box_109_272_427_587.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F6c6459f20a6cb3c70c9142bc37401c0f198458b833b87538a248e11ba1a5e3b9" alt="Image" width="26%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//79c4fa05-bd5e-4cb8-bb43-0bdf78f7d216/markdown_0/imgs/img_in_image_box_445_270_1007_588.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fc5c6428047fcab5292cd6a12a92b5081490bd54c5a13de67b95a46ab757a2878" alt="Image" width="47%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片3</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//79c4fa05-bd5e-4cb8-bb43-0bdf78f7d216/markdown_0/imgs/img_in_image_box_109_686_426_1003.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fc9d407e12a6d45060d3977a445e92956099eb6c5b08f103e014012e8d7fa2219" alt="Image" width="26%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//79c4fa05-bd5e-4cb8-bb43-0bdf78f7d216/markdown_0/imgs/img_in_image_box_447_684_1006_1005.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2Fdb965a4005e87d0aad277eca44f1cd33fd62b21c3cc50fa9b092ae5b5b904391" alt="Image" width="46%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片4</div> </div>


##### [提示词]

参考 图片3 中的分镜构图，女孩正在等爸爸做好饭，她说：“，！？”，女孩形象参考图片1。接着镜头向右横摇，切换至 图片4 的画面和构图，爸爸形象参考 图片2，爸爸回答她：“，！“，接着镜头切换回女儿略显失落的面部表情特写，她说：“？。。。”，接着切换成爸爸的面部特写，他说：“。。” "！”。

## 04 视频参考

Seedance 2.0 系列模型支持视频参考，使用时指代清楚生成内容和参考对象即可。

使用过程中，如对视频顺序有要求，应按顺序上传，提示词中可使用 视频1 、 视频2 …… 视频n 进行准确指代。

### 4.1 动作参考

提示词参考模板：

Plain

参考「视频n」的「动作描述」，生成「画面描述」，保持动作细节一致。

##### 参考案例：

影视

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f99ac5ba-94c0-466c-b0a3-ebb5eed11445/markdown_0/imgs/img_in_image_box_111_471_1014_981.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F87bb350ea8d069d124e2c839cadea35f360d1a4f309242f6364b9fa7adc2d399" alt="Image" width="75%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2d1d1baf-5bcc-4706-88f7-6a1e20f19a7d/markdown_0/imgs/img_in_image_box_112_143_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F2b9b8d14b1c661ad369a872d68b2c8c2222bb8c06d898f6e73645fd132f6ef4a" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2d1d1baf-5bcc-4706-88f7-6a1e20f19a7d/markdown_0/imgs/img_in_image_box_146_699_587_1134.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F75b4f36f610a1538d2448ce3e42690842cb6480bbcace7d33bb9dc8a7bf46233" alt="Image" width="37%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2d1d1baf-5bcc-4706-88f7-6a1e20f19a7d/markdown_0/imgs/img_in_image_box_602_698_1043_1135.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2Fd529aeb1f8d0810845e323e3b31783f4090d56add472da1fef91d9e8fc34570a" alt="Image" width="37%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片2</div> </div>


##### [提示词]

参考 视频1 的人物动作和镜头语言，生成 图片2 和 图片1 的打斗场面， 图片2 是左边人物， 图片1 是右边人物。有激烈的背景音乐。

营销

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//0553f9b1-02ff-4a19-9c79-f9fbc53613ee/markdown_0/imgs/img_in_image_box_112_144_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A28Z%2F-1%2F%2Fe399af9651a7432ecf8891213a4a4449a9c21c85381be289bb744a01191586ce" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//0553f9b1-02ff-4a19-9c79-f9fbc53613ee/markdown_0/imgs/img_in_image_box_111_720_1015_1226.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A28Z%2F-1%2F%2F94caf76f46990cffb4fb8a7af8e2286ace52ae891af4690e0c90e498c9e46e0a" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


##### [提示词]

参考 视频1 中马的奔跑形态，生成一匹金色的骏马在草原上奔跑，随即定格其奔跑的华丽姿态，变成一个马形的金吊坠。

### 4.2 运镜参考

提示词参考模板：

Plain

参考「视频n」的「运镜描述」，生成「画面描述」，保持运镜一致。

参考案例：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//37905ddd-efea-40b9-a1ab-c397d3840c8d/markdown_0/imgs/img_in_image_box_109_368_1016_878.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F0ef164dea9b4bb651fcc010b12cb6d103c4980fd3609716f473426256af0fbb8" alt="Image" width="76%" /></div>


##### [提示词]

参考 视频1 的运镜，做一个科技园区的概念视频，以 图片1 中的高楼为视觉中心，同为第一视角俯冲，体现出 图片1 中园区的科技感。

##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//33e9d953-ab8f-441b-b81f-9d0cfda4b240/markdown_0/imgs/img_in_image_box_111_143_1013_650.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F134fb2ffa6b4a7669320b96cc9ff3582c7d632a449f49af4823868aa3e35ba6a" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//33e9d953-ab8f-441b-b81f-9d0cfda4b240/markdown_0/imgs/img_in_image_box_112_718_1077_1261.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2Fdd9bda4e52eb663d9e2b1f594e753d6981bf0106465a8568adc1485a14d2d0c8" alt="Image" width="81%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


### 4.3 特效参考

提示词参考模板：

Plain

参考「视频n」的「特效描述」，生成「画面描述」，保持特效一致。

##### 参考案例：

影视

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//22659d2a-9456-4494-8093-a27a2c42d2b1/markdown_0/imgs/img_in_image_box_111_471_1014_981.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A28Z%2F-1%2F%2F04d3a574b7acdf6f77009d956c93924e95d7ac0a7d8ebaa09abebf76d6cdb4ef" alt="Image" width="75%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f0ae6fce-03d9-4d0f-a244-0ad03a703154/markdown_0/imgs/img_in_image_box_112_143_1013_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2Fedb148c4511ece4b36743d23c0663f5c7574a8f88cd9c3477c0665a03747b679" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f0ae6fce-03d9-4d0f-a244-0ad03a703154/markdown_0/imgs/img_in_image_box_113_720_1077_1260.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F0d366465edde7cd605f4894963cd0da6656d471309f868cf05ab0b668aad95c3" alt="Image" width="80%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


##### [提示词]

参考 视频1 的金色粒子特效，让 图片2 中的人物吹笛子的同时，身边环绕一样的粒子特效。

##### 玩法特效

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f8d8ba4c-81db-4ed2-b0a3-74f6fcb11d50/markdown_0/imgs/img_in_image_box_111_172_1014_677.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A24Z%2F-1%2F%2F5517a977be97561e4bb5cfc43f47654a261879101abf09988e6d2a2349a407bd" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f8d8ba4c-81db-4ed2-b0a3-74f6fcb11d50/markdown_0/imgs/img_in_image_box_111_744_1017_1251.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A24Z%2F-1%2F%2F5cf4e24c9fdc6f317069ec72e1b5d4cf6bba8969d11c5cf836f0c47c67da36dd" alt="Image" width="76%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//35a7038f-7812-4a26-85f0-f9334fdf628c/markdown_0/imgs/img_in_image_box_146_145_1042_646.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F9e03c4cc2db67a4011ccdbb5fd80ea902131f45961040091345eaadba30ad451" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


[提示词]

参考 视频1 的特效，让 图片1 中的女生长出相同的翅膀，翅膀生成轨迹一致。

## 05 视频编辑

Seedance 2.0 系列模型支持视频编辑，支持增加、删除或修改元素，视频的向前或向后延长，以及轨道补齐。

使用过程中，如对视频顺序有要求，应按顺序上传，提示词中可使用 视频1 、 视频2 …… 视频n 进行准确指代。

### 5.1 元素增删改

提示词参考模板：

Plain

增加元素：在「视频n」的「时间位置」+「空间位置」，增加「理想元素描述」。

删除元素：删除「视频n」中的「被删除元素」，视频其他内容保持不变。

修改元素：将「视频n」中的「被更换元素描述」，替换为「理想元素描述」。

参考案例：

增加元素

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a8a5d7d2-cf93-47ff-90ec-6db1d4b8b199/markdown_0/imgs/img_in_image_box_112_144_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2Fee4f2e12e7b5fb7b2d3e84307cee662b260f3dd00a03c8a02cbf637c2cba7458" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//a8a5d7d2-cf93-47ff-90ec-6db1d4b8b199/markdown_0/imgs/img_in_image_box_111_718_1017_1227.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2F72362c856235918924b37a97c767071b49ba0311ccfac726e48465b93d2e59b7" alt="Image" width="76%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


##### [提示词]

在 视频1 的台面上添加炸鸡、披萨等小吃。

##### 删除元素

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//ccad43d4-4dae-47a9-bc0a-80264130f4d2/markdown_0/imgs/img_in_image_box_112_143_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2F509e9f659f12ef04d880bd740e19ce46ba9618cd6757e31195e54264fb0b3e31" alt="Image" width="75%" /></div>


##### [参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//ccad43d4-4dae-47a9-bc0a-80264130f4d2/markdown_0/imgs/img_in_image_box_111_718_1017_1226.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2Fe1b30cad18ad37fe34de2e62e0803d67021b3e8d0c9e8c3bb15f2d1476d47173" alt="Image" width="76%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


##### [提示词]

清除 视频1 桌面上的其他零件和工具，保持桌面整洁干净，桌面上只有他俩手里的。

##### 修改元素

##### [成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f845cbc8-e5b9-4cbd-83b8-859be43f9c9c/markdown_0/imgs/img_in_image_box_112_144_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2Fc84fe54c4a98c25c271e184778290e1979d461887cc4b15685a7f2f77a2394e0" alt="Image" width="75%" /></div>


##### [參考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//f845cbc8-e5b9-4cbd-83b8-859be43f9c9c/markdown_0/imgs/img_in_image_box_111_718_1017_1227.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F4cc85f04ea57d3ac76484174fd1c43289955b18d00ce26ae04230696bc8e7327" alt="Image" width="76%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//6903c174-0370-4e46-8076-db9e2a8bd4cb/markdown_0/imgs/img_in_image_box_114_145_1077_1108.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A27Z%2F-1%2F%2F748aad4417a840998fac138865340330b9059ce11b97b5e47b79fafea1f28815" alt="Image" width="80%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲图片1</div> </div>


##### [提示词]

将 视频1 中的香水替换成 图片1 中的面霜，动作和运镜不变。

### 5.2 视频延长

提示词参考模板：

Plain

- 向前/向后延长「视频n」+「需延长的视频描述」

- 生成「视频n」之前/之后的内容+「需延长的视频描述」

##### 注意

模型将自动截取衔接部分进行合成，输入视频原有片段，不会重复生成。

##### 参考案例：

向后延长

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//e148091a-49d1-4f77-bd0a-8cba1200b1ee/markdown_0/imgs/img_in_image_box_111_471_1014_981.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A26Z%2F-1%2F%2Fa7060ddbd5f12ab776707c0ef754450935533fc05ab78768eb36bfa63403d724" alt="Image" width="75%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//47aa7c4e-2744-4cd9-8910-02aa2886c9de/markdown_0/imgs/img_in_image_box_111_143_1014_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F95d62c54f99b3a423f592a8f82950816c07da8725cfcc237a910ecb3cb591789" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


##### [提示词]

生成 视频1 之后的内容，迟到的两个男士跑向他们，五个人终于见面，友好聊天。

向前延长

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//47aa7c4e-2744-4cd9-8910-02aa2886c9de/markdown_0/imgs/img_in_image_box_110_942_1015_1452.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F80389c68cf6721e91e12d318839c0b8489b75a84c83b08fbf981366a6e9c6b8d" alt="Image" width="75%" /></div>


[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2af7414b-6c14-466c-bdc8-2abb2fa7492f/markdown_0/imgs/img_in_image_box_111_143_1013_651.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A23Z%2F-1%2F%2F84b8fdc5f4c8b9e5c92d775eaef253126255a1adc792735f9df422ad7de5d918" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


##### [提示词]

向前延长 视频1 ，给白衣男子过肩镜头，白衣男子说：“It’s not that bad. You're just stressed. Everyone goes through this, you just need to keep going.”

### 5.3 轨道补齐

提示词参考模板：

Plain

「视频1」+「过渡画面描述」+接「视频2」+「过渡画面描述」+接「视频3」

说明

· Seedance 2.0 系列模型最多支持 3 段视频输入，总时长不得超过 15 秒。

· 生成时将自动截取首尾视频的衔接部分，仅保留必要片段参与合成。

参考案例：

[成品效果]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2a7c85fa-c133-4c4e-8b51-cdba2b304c21/markdown_0/imgs/img_in_image_box_111_143_1013_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2F26d4dbc13062e79dc7a2efbf875cd4e3bf15999c473f34a3f880005aad21846b" alt="Image" width="75%" /></div>


[提示词]

视频1，树叶落地的瞬间，激起金色粒子特效，一阵风吹过，接视频2。

[参考素材]

<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//2a7c85fa-c133-4c4e-8b51-cdba2b304c21/markdown_0/imgs/img_in_image_box_110_839_1016_1349.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A25Z%2F-1%2F%2F9afdf2d0814875a69ab1fba366325a8a25b061b9c2a0c1369e8057d2f48b2f94" alt="Image" width="76%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 1</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//63da6c18-ede9-4eed-88e4-0c936c4185f9/markdown_0/imgs/img_in_image_box_111_143_1014_652.jpg?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-04-26T07%3A21%3A22Z%2F-1%2F%2F254ebcd5a69ca00052b850aee497e970f97509465a722d028fcf613e180fddf0" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">▲ 视频 2</div> </div>
