from re     import sub
from random import randint
from utils.base import node_b64

class LZWCompressor:
    def __init__(self):
        self.current_bit_index  = 0
        self.buffer             = 0
        self.output_bytes       = []
        self.codebook           = {chr(a): a for a in range(256)}
        self.bit_length         = 8
        self.next_code          = 255

    def write(self, code, code_length):
        while code_length > 0:
            if code & 1:
                self.buffer |= 1 << self.current_bit_index
            code >>= 1
            self.current_bit_index += 1
            if self.current_bit_index == 8:
                self.output_bytes.append(self.buffer)
                self.current_bit_index = 0
                self.buffer = 0
                
            code_length -= 1

    def compress(self, data) -> list:
        index = 0
        while index < len(data):
            chunk = data[index]
            while index + 1 < len(data) and chunk + data[index + 1] in self.codebook:
                index += 1
                chunk += data[index]

            self.write(self.codebook[chunk], self.bit_length)
            if index + 1 == len(data):
                break

            self.next_code += 1

            if self.next_code & (self.next_code - 1) == 0:
                self.bit_length += 1

            self.codebook[chunk + data[index + 1]] = self.next_code
            index += 1
            
        if self.current_bit_index > 0:
            self.output_bytes.append(self.buffer)

        return self.output_bytes

    
def b64_shift(b64_string):
    return sub(r"[A-Za-z0-9+/=]",
        lambda shift_table: "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="[ 
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".index(shift_table.group(0))
        ], b64_string
    )

def b64_unshift(b64_string):
    return sub(r"[A-Za-z0-9+/=]",
        lambda shift_table: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="[ 
            "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=".index(shift_table.group(0))
        ], b64_string
    )

def rc4_crypt(plain_text: str, key: str) -> str:
    s_box           = [_ for _ in range(256)]
    j               = 0
    encrypted_text  = ""
    
    for i in range(256):
        j        = (j + s_box[i] + ord(key[i % len(key)])) % 256
        temp     = s_box[i]
        s_box[i] = s_box[j]
        s_box[j] = temp

    i = 0
    j = 0
    for index in range(len(plain_text)):
        i        = (i + 1) % 256
        j        = (j + s_box[i]) % 256
        temp     = s_box[i]
        s_box[i] = s_box[j]
        s_box[j] = temp
        
        encrypted_text += chr(255 & (ord(plain_text[index]) ^ s_box[(s_box[i] + s_box[j]) % 256]))

    return encrypted_text

def mssdk_enc(plain_text: str):
    key     = chr(66) #chr(randint(0, 255))
    rc4_enc = rc4_crypt(plain_text, key)
    b64_enc = node_b64("A" + key + rc4_enc)
    
    return b64_shift(b64_enc)

def report_enc(base_string):
    return mssdk_enc(base_string) 

if __name__ == '__main__':

    mssdk_data      = '''{"tokenList":[],"navigator":{"appCodeName":"Mozilla","appMinorVersion":"undefined","appName":"Netscape","appVersion":"5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","buildID":"undefined","doNotTrack":"null","msDoNotTrack":"undefined","oscpu":"undefined","platform":"MacIntel","product":"Gecko","productSub":"20030107","cpuClass":"undefined","vendor":"Google Inc.","vendorSub":"","deviceMemory":"8","language":"en","systemLanguage":"undefined","userLanguage":"undefined","webdriver":"false","hardwareConcurrency":8,"maxTouchPoints":0,"cookieEnabled":1,"vibrate":3,"credentials":99,"storage":99,"requestMediaKeySystemAccess":3,"bluetooth":99,"languages":"en,fr-FR,es-ES,es,fr,en-US,am,de","touchEvent":2,"touchstart":2},"wID":{"permState":"prompt","load":3,"nap":"01321044241322243122","rtcIP":"80.215.202.5","nativeLength":33,"nativeName":2,"jsFontsList":"1","syntaxError":"Failed to construct 'WebSocket': The URL 'Create WebSocket' is invalid.","timestamp":"1678381304166","timezone":0,"magic":3,"canvas":"3558723902","wProps":374198,"dProps":2,"jsv":"","browserType":16,"iframe":2,"pppt":2,"rtt":2,"notifyPerm":"default","sdkVersion":"4.4.4","scmVersion":"1.0.0.28","aid":1988,"msgType":1,"privacyMode":513,"aidList":[1988],"isf":2,"env":"11111111111111111111111","propLength":{"a":1109,"b":1059,"c":871,"d":10,"e":872,"f":0},"objProx":"11111111111111111","sri":1,"index":69},"window":{"Image":3,"isSecureContext":1,"ActiveXObject":4,"toolbar":99,"locationbar":99,"external":99,"mozRTCPeerConnection":4,"postMessage":3,"webkitRequestAnimationFrame":3,"BluetoothUUID":3,"netscape":4,"localStorage":99,"sessionStorage":99,"indexedDB":99,"devicePixelRatio":2,"devicePixelRatioFloat":2,"location":"https://www.tiktok.com/@onlpx/video/7068338816213355781"},"webgl":{"supportedExtensions":["ANGLE_instanced_arrays","EXT_blend_minmax","EXT_color_buffer_half_float","EXT_disjoint_timer_query","EXT_float_blend","EXT_frag_depth","EXT_shader_texture_lod","EXT_texture_compression_rgtc","EXT_texture_filter_anisotropic","EXT_sRGB","KHR_parallel_shader_compile","OES_element_index_uint","OES_fbo_render_mipmap","OES_standard_derivatives","OES_texture_float","OES_texture_float_linear","OES_texture_half_float","OES_texture_half_float_linear","OES_vertex_array_object","WEBGL_color_buffer_float","WEBGL_compressed_texture_s3tc","WEBGL_compressed_texture_s3tc_srgb","WEBGL_debug_renderer_info","WEBGL_debug_shaders","WEBGL_depth_texture","WEBGL_draw_buffers","WEBGL_lose_context","WEBGL_multi_draw"],"antialias":1,"blueBits":8,"depthBits":24,"greenBits":8,"maxAnisotropy":16,"maxCombinedTextureImageUnits":32,"maxCubeMapTextureSize":16384,"maxFragmentUniformVectors":1024,"maxRenderbufferSize":16384,"maxTextureImageUnits":16,"maxTextureSize":16384,"maxVaryingVectors":31,"maxVertexAttribs":16,"maxVertexTextureImageUnits":16,"maxVertexUniformVectors":1024,"shadingLanguageVersion":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)","stencilBits":0,"version":"WebGL 1.0 (OpenGL ES 2.0 Chromium)","vendor":"Google Inc. (Apple)","renderer":"ANGLE (Apple, Apple M2, OpenGL 4.1)"},"document":{"characterSet":"UTF-8","compatMode":"CSS1Compat","documentMode":"undefined","URL":"https://www.tiktok.com/@onlpx/video/7068338816213355781","layers":4,"all":12,"images":99},"screen":{"innerWidth":320,"innerHeight":841,"outerWidth":1470,"outerHeight":920,"screenX":0,"screenY":36,"pageXOffset":0,"pageYOffset":0,"availWidth":1470,"availHeight":924,"sizeWidth":1470,"sizeHeight":956,"clientWidth":320,"clientHeight":6355,"colorDepth":30,"pixelDepth":30,"focus":2,"hidden":2,"visibilityState":"visible","location":1,"menubar":1,"scrollbar":0,"orientation":"landscape-primary"},"plugins":{"plugin":["internal-pdf-viewer|application/pdf|pdf","internal-pdf-viewer|text/pdf|pdf","internal-pdf-viewer|application/pdf|pdf","internal-pdf-viewer|text/pdf|pdf","internal-pdf-viewer|application/pdf|pdf","internal-pdf-viewer|text/pdf|pdf","internal-pdf-viewer|application/pdf|pdf","internal-pdf-viewer|text/pdf|pdf","internal-pdf-viewer|application/pdf|pdf","internal-pdf-viewer|text/pdf|pdf"],"pv":"0","proto":1},"custom":{},"canvasIntegrity":{"a":1,"b":1,"c":1,"d":["305534646","305534646"],"e":1},"mediaQuery":{"dppx":2,"orientation":"portrait","hover":"hover","anyPointer":"fine","maxHeight":841,"maxWidth":320,"dpi":192},"env":"","propLength":{},"objProx":"","battery":{"charging":2,"level":61,"chargingTime":"Infinity","dischargingTime":"19980"},"msgMeta":{"msgType":1,"msgSrcProp":2,"msgProtocol":1,"aid":1988,"aidList":[1988]}}'''
    enc = report_enc(mssdk_data) #.replace('f6sm1', 'fLsm1')

    from time import time
    from requests import post
    payload = {
        "magic"         : 538969122,
        "version"       : 1,
        "dataType"      : 8,
        "strData"       : enc,
        "tspFromClient" : int(time() * 1000)
    }

    headers = {
        'authority' : 'mssdk-va.tiktok.com',
        'origin'    : 'https://www.tiktok.com',
        'referer'   : 'https://www.tiktok.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }


    response = post('https://mssdk-va.tiktok.com/web/report?msToken=ct3W3Lghq0qv5THWL14G9RwsqLHQJjL0FpJGgc8amPfTNbMEQy7gQuXSMqnmoVPxs9D4MxPQ1DfGHAZZBntoSFa80q_Q-xeGufsws8ZQ-bmmf2mlp1Fheexe3d3gC8C6bn7b2BJVwd9tdj3O&X-Bogus=DFSzswVYg9yq3-8USgDtBV/F6qHh',
        headers=headers,
        json=payload
    )

    print(response.json())
