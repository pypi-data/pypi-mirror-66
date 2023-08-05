# -*- coding: utf-8 -*-
DESC = "tmt-2018-03-21"
INFO = {
  "TextTranslate": {
    "params": [
      {
        "name": "SourceText",
        "desc": "待翻译的文本，文本统一使用utf-8格式编码，非utf-8格式编码字符会翻译失败，请传入有效文本，html标记等非常规翻译文本会翻译失败。单次请求的文本长度需要低于2000。"
      },
      {
        "name": "Source",
        "desc": "源语言，参照Target支持语言列表"
      },
      {
        "name": "Target",
        "desc": "目标语言，参照支持语言列表\n<li> zh : 简体中文 </li> <li> zh-TW : 繁体中文 </li><li> en : 英文 </li><li> jp : 日语 </li> <li> kr : 韩语 </li><li> de : 德语 </li><li> fr : 法语 </li><li> es : 西班牙文 </li> <li> it : 意大利文 </li><li> tr : 土耳其文 </li><li> ru : 俄文 </li><li> pt : 葡萄牙文 </li><li> vi : 越南文 </li><li> id : 印度尼西亚文 </li><li> ms : 马来西亚文 </li><li> th : 泰文 </li><li> auto : 自动识别源语言，只能用于source字段 </li>"
      },
      {
        "name": "ProjectId",
        "desc": "项目ID，可以根据控制台-账号中心-项目管理中的配置填写，如无配置请填写默认项目ID:0"
      },
      {
        "name": "UntranslatedText",
        "desc": "用来标记不希望被翻译的文本内容，如句子中的特殊符号、人名、地名等；每次请求只支持配置一个不被翻译的单词；仅支持配置人名、地名等名词，不要配置动词或短语，否则会影响翻译结果。"
      }
    ],
    "desc": "提供中文到英文、英文到中文的等多种语言的文本内容翻译服务， 经过大数据语料库、多种解码算法、翻译引擎深度优化，在新闻文章、生活口语等不同语言场景中都有深厚积累，翻译结果专业评价处于行业领先水平。<br />\n提示：对于一般开发者，我们建议优先使用SDK接入简化开发。SDK使用介绍请直接查看 5. 开发者资源 部分。\n"
  },
  "ImageTranslate": {
    "params": [
      {
        "name": "SessionUuid",
        "desc": "唯一id，返回时原样返回"
      },
      {
        "name": "Scene",
        "desc": "doc:文档扫描"
      },
      {
        "name": "Data",
        "desc": "图片数据的Base64字符串，图片大小上限为4M，建议对源图片进行一定程度压缩"
      },
      {
        "name": "Source",
        "desc": "源语言，支持语言列表<li> zh : 中文 </li> <li> en : 英文 </li>"
      },
      {
        "name": "Target",
        "desc": "目标语言，支持语言列表<li> zh : 中文 </li> <li> en : 英文 </li>"
      },
      {
        "name": "ProjectId",
        "desc": "项目ID，可以根据控制台-账号中心-项目管理中的配置填写，如无配置请填写默认项目ID:0"
      }
    ],
    "desc": "提供中文到英文、英文到中文两种语言的图片翻译服务，可自动识别图片中的文本内容并翻译成目标语言，识别后的文本按行翻译，后续会提供可按段落翻译的版本。<br />\n提示：对于一般开发者，我们建议优先使用SDK接入简化开发。SDK使用介绍请直接查看 5. 开发者资源 部分。"
  },
  "LanguageDetect": {
    "params": [
      {
        "name": "Text",
        "desc": "待识别的文本，文本统一使用utf-8格式编码，非utf-8格式编码字符会翻译失败。单次请求的文本长度需要低于2000。"
      },
      {
        "name": "ProjectId",
        "desc": "项目ID，可以根据控制台-账号中心-项目管理中的配置填写，如无配置请填写默认项目ID:0"
      }
    ],
    "desc": "可自动识别文本内容的语言种类，轻量高效，无需额外实现判断方式，使面向客户的服务体验更佳。 <br />\n提示：对于一般开发者，我们建议优先使用SDK接入简化开发。SDK使用介绍请直接查看 5. 开发者资源 部分。"
  },
  "SpeechTranslate": {
    "params": [
      {
        "name": "SessionUuid",
        "desc": "一段完整的语音对应一个SessionUuid"
      },
      {
        "name": "Source",
        "desc": "音频中的语言类型，支持语言列表<li> zh : 中文 </li> <li> en : 英文 </li>"
      },
      {
        "name": "Target",
        "desc": "翻译目标语⾔言类型 ，支持的语言列表<li> zh : 中文 </li> <li> en : 英文 </li>"
      },
      {
        "name": "AudioFormat",
        "desc": "pcm : 146   amr : 33554432   mp3 : 83886080"
      },
      {
        "name": "Seq",
        "desc": "语音分片的序号，从0开始"
      },
      {
        "name": "IsEnd",
        "desc": "是否最后一片语音分片，0-否，1-是"
      },
      {
        "name": "Data",
        "desc": "语音分片内容的base64字符串，音频内容应含有效并可识别的文本"
      },
      {
        "name": "ProjectId",
        "desc": "项目ID，可以根据控制台-账号中心-项目管理中的配置填写，如无配置请填写默认项目ID:0"
      },
      {
        "name": "Mode",
        "desc": "识别模式，该参数已废弃"
      }
    ],
    "desc": "本接口提供音频内文字识别 + 翻译功能，目前开放中英互译的语音翻译服务。\n待识别和翻译的音频文件可以是 pcm、mp3、amr和speex 格式，采样率要求16kHz、位深16bit、单声道，音频内语音清晰。<br/>\n如果采用流式传输的方式，要求每个分片时长200ms~500ms；如果采用非流式的传输方式，要求音频时长不超过8s。注意最后一个分片的IsEnd参数设置为1。<br />\n提示：对于一般开发者，我们建议优先使用SDK接入简化开发。SDK使用介绍请直接查看 5. 开发者资源部分。\n"
  },
  "TextTranslateBatch": {
    "params": [
      {
        "name": "Source",
        "desc": "源语言，参照Target支持语言列表"
      },
      {
        "name": "Target",
        "desc": "目标语言，参照支持语言列表\n<li> zh : 简体中文 </li> <li> zh-TW : 繁体中文 </li><li> en : 英文 </li><li> jp : 日语 </li> <li> kr : 韩语 </li><li> de : 德语 </li><li> fr : 法语 </li><li> es : 西班牙文 </li> <li> it : 意大利文 </li><li> tr : 土耳其文 </li><li> ru : 俄文 </li><li> pt : 葡萄牙文 </li><li> vi : 越南文 </li><li> id : 印度尼西亚文 </li><li> ms : 马来西亚文 </li><li> th : 泰文 </li><li> auto : 自动识别源语言，只能用于source字段 </li>"
      },
      {
        "name": "ProjectId",
        "desc": "项目ID，可以根据控制台-账号中心-项目管理中的配置填写，如无配置请填写默认项目ID:0"
      },
      {
        "name": "SourceTextList",
        "desc": "待翻译的文本列表，批量接口可以以数组方式在一次请求中填写多个待翻译文本。文本统一使用utf-8格式编码，非utf-8格式编码字符会翻译失败，请传入有效文本，html标记等非常规翻译文本会翻译失败。单次请求的文本长度总和需要低于2000。"
      }
    ],
    "desc": "文本翻译的批量接口"
  }
}