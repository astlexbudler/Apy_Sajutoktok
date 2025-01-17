/*

1. SHA256 문자 암호화
SHA256(일반 문자열) => 암호화된 문자열(300글자)

2. csrf 토큰
csrftoken으로 API 요청

3. getNowDt, compareDates 날짜함수
getNowDt => 2023-12-01 13:07 과 같이(Python에서 사용하는 날짜 포멧과 동일) 현재 시간 정보 출력
compareDates => dayString1 - dayString2를 수행. 차이가 나는 날짜 출력(시간 x)
getTimestamp() => 1705456741633

4. 사전 정의된 API들
clearSession() 세션 초기화

5. 사전 정의된 Modal들
askLogin() 로그인 물어보기
askLogout() 로그아웃 물어보기
loginSuccess() 로그인 성공
loginFail() 로그인 실패
serverError() 서버 오류
serverDenied() 접근 거부
checkImage(file) 이미지 검사
checkVideo(file) 비디오 검사

6. 기타
askInitMessage() 모든 알림 삭제

7. ORMS
sort_tables()
uploadFile()
getData()
setData()
deleteData()
orm_doctor()

toggleInfo() => 정보 토글

*/

// //////////////////////////////////////////////////
// SHA256 문자 암호화
function SHA256(s) {

    var chrsz = 8;
    var hexcase = 0;

    function safe_add(x, y) {
        var lsw = (x & 0xFFFF) + (y & 0xFFFF);
        var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
        return (msw << 16) | (lsw & 0xFFFF);
    }

    function S(X, n) { return (X >>> n) | (X << (32 - n)); }
    function R(X, n) { return (X >>> n); }
    function Ch(x, y, z) { return ((x & y) ^ ((~x) & z)); }
    function Maj(x, y, z) { return ((x & y) ^ (x & z) ^ (y & z)); }
    function Sigma0256(x) { return (S(x, 2) ^ S(x, 13) ^ S(x, 22)); }
    function Sigma1256(x) { return (S(x, 6) ^ S(x, 11) ^ S(x, 25)); }
    function Gamma0256(x) { return (S(x, 7) ^ S(x, 18) ^ R(x, 3)); }
    function Gamma1256(x) { return (S(x, 17) ^ S(x, 19) ^ R(x, 10)); }

    function core_sha256(m, l) {

        var K = new Array(0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1,
            0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
            0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786,
            0xFC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
            0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
            0x6CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
            0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B,
            0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
            0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A,
            0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
            0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2);

        var HASH = new Array(0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19);

        var W = new Array(64);
        var a, b, c, d, e, f, g, h, i, j;
        var T1, T2;

        m[l >> 5] |= 0x80 << (24 - l % 32);
        m[((l + 64 >> 9) << 4) + 15] = l;

        for (var i = 0; i < m.length; i += 16) {
            a = HASH[0];
            b = HASH[1];
            c = HASH[2];
            d = HASH[3];
            e = HASH[4];
            f = HASH[5];
            g = HASH[6];
            h = HASH[7];

            for (var j = 0; j < 64; j++) {
                if (j < 16) W[j] = m[j + i];
                else W[j] = safe_add(safe_add(safe_add(Gamma1256(W[j - 2]), W[j - 7]), Gamma0256(W[j - 15])), W[j - 16]);

                T1 = safe_add(safe_add(safe_add(safe_add(h, Sigma1256(e)), Ch(e, f, g)), K[j]), W[j]);
                T2 = safe_add(Sigma0256(a), Maj(a, b, c));

                h = g;
                g = f;
                f = e;
                e = safe_add(d, T1);
                d = c;
                c = b;
                b = a;
                a = safe_add(T1, T2);
            }

            HASH[0] = safe_add(a, HASH[0]);
            HASH[1] = safe_add(b, HASH[1]);
            HASH[2] = safe_add(c, HASH[2]);
            HASH[3] = safe_add(d, HASH[3]);
            HASH[4] = safe_add(e, HASH[4]);
            HASH[5] = safe_add(f, HASH[5]);
            HASH[6] = safe_add(g, HASH[6]);
            HASH[7] = safe_add(h, HASH[7]);
        }
        return HASH;
    }

    function str2binb(str) {
        var bin = Array();
        var mask = (1 << chrsz) - 1;
        for (var i = 0; i < str.length * chrsz; i += chrsz) {
            bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << (24 - i % 32);
        }
        return bin;
    }

    function Utf8Encode(string) {
        string = string.replace(/\r\n/g, "\n");
        var utftext = "";

        for (var n = 0; n < string.length; n++) {

            var c = string.charCodeAt(n);

            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if ((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }

        }

        return utftext;
    }

    function binb2hex(binarray) {
        var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
        var str = "";
        for (var i = 0; i < binarray.length * 4; i++) {
            str += hex_tab.charAt((binarray[i >> 2] >> ((3 - i % 4) * 8 + 4)) & 0xF) +
                hex_tab.charAt((binarray[i >> 2] >> ((3 - i % 4) * 8)) & 0xF);
        }
        return str;
    }

    s = Utf8Encode(s);
    return binb2hex(core_sha256(str2binb(s), s.length * chrsz));

}



// //////////////////////////////////////////////////
// SHA256 문자 암호화
getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



// //////////////////////////////////////////////////
// 날짜 함수들
function getNowDt() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1; // 월은 0부터 시작하므로 1을 더해야 함
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();

    // 월, 일, 시간, 분이 10보다 작으면 앞에 0을 붙임
    month = month < 10 ? '0' + month : month;
    day = day < 10 ? '0' + day : day;
    hour = hour < 10 ? '0' + hour : hour;
    minute = minute < 10 ? '0' + minute : minute;

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
}

function getFullDt() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1; // 월은 0부터 시작하므로 1을 더해야 함
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var millisecond = now.getMilliseconds();

    // 월, 일, 시간, 분이 10보다 작으면 앞에 0을 붙임
    month = month < 10 ? '0' + month : month;
    day = day < 10 ? '0' + day : day;
    hour = hour < 10 ? '0' + hour : hour;
    minute = minute < 10 ? '0' + minute : minute;
    second = second < 10 ? '0' + second : second;
    millisecond = millisecond < 10 ? '00' + millisecond : millisecond < 100 ? '0' + millisecond : millisecond;

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second + '.' + millisecond;
}

function compareDates(dateTimeString1, dateTimeString2) {
    // 문자열을 Date 객체로 변환
    var date1 = new Date(dateTimeString1);
    var date2 = new Date(dateTimeString2);

    // 날짜 차이 계산 (밀리초 단위)
    var diff = date2 - date1;

    // dateTimeString1이 더 최근이면 -1 반환
    if (diff < 0) {
        return -1;
    }

    // 밀리초를 일 단위로 변환 (1일 = 24시간 * 60분 * 60초 * 1000밀리초)
    var diffDays = Math.floor(diff / (24 * 60 * 60 * 1000));

    return diffDays;
}

function getTimestamp() {
    return new Date().getTime();
}



// //////////////////////////////////////////////////
// 사전 정의 API
logout = () => {
    fetch("/api/logout").then(() => {
        window.location.href = '/';
    });
}



// //////////////////////////////////////////////////
// 사전 정의 모달
askLogin = () => {
    document.location.href = "/login";
}

askLogout = () => {
    clearSession();
}

loginSuccess = () => {
    Swal.fire({
        html: `
<div class="mt-4">
    <!-- 제목 -->
    <div class="text-center pb-4">
        <h1 class="text-dark">로그인 성공</h1>
    </div>
    <!-- 내용 -->
    <diV class="text-start">
        <p class="text-secondary">
            로그인되었습니다.
        </p>
    </div>
</div>`,
        icon: 'success',
        showConfirmButton: true,
        confirmButtonText: '확인',
        showCancelButton: false,
        cancelButtonText: ``
      })
      .then((result) => {
        if (result.isConfirmed) {
            document.location.href = "/main";
        }
      });
}

loginFail = () => {
    Swal.fire({
        html: `
<div class="mt-4">
    <!-- 제목 -->
    <div class="text-center pb-4">
        <h1 class="text-dark">로그인 실패</h1>
    </div>
    <!-- 내용 -->
    <diV class="text-start">
        <p class="text-secondary">
            로그인 할 수 없습니다.<br>
            아이디 또는 비밀번호를 확인해주세요.
        </p>
    </div>
</div>`,
        icon: 'error',
        showConfirmButton: true,
        confirmButtonText: '확인',
        showCancelButton: false,
        cancelButtonText: ``
      });
}

serverError = () => {
    Swal.fire({
        html: `
<div class="mt-4">
    <!-- 제목 -->
    <div class="text-center pb-4">
        <h1 class="text-dark">서버 오류</h1>
    </div>
    <!-- 내용 -->
    <diV class="text-start">
        <p class="text-secondary">
            알 수 없는 이유로 오류가 발생했습니다.<br>
            이 메세지가 계속 발생할 경우 담당자 또는 아래 연락처로 문의주세요.<br>
            <br>
            애플리파이IDS<br>
            master@applifyids.com<br>
            070-7557-7779
        </p>
    </div>
</div>`,
        icon: 'error',
        showConfirmButton: true,
        confirmButtonText: '확인',
        showCancelButton: false,
        cancelButtonText: ``
      });
}

serverDenied = () => {
    Swal.fire({
        html: `
<div class="mt-4">
    <!-- 제목 -->
    <div class="text-center pb-4">
        <h1 class="text-dark">요청 거부</h1>
    </div>
    <!-- 내용 -->
    <diV class="text-start">
        <p class="text-secondary">
        서버로부터 요청이 거부되었습니다.<br>
        잠시 후 다시 시도해주세요.
        </p>
    </div>
</div>`,
        icon: 'error',
        showConfirmButton: true,
        confirmButtonText: '확인',
        showCancelButton: false,
        cancelButtonText: ``
      });
}

checkImage = (file) => {
    try {
        if (file.type.startsWith('image/')) {
            imageOk = false;
            return true
        } else {
            return false
        }
    } catch {
        return false
    }
}

checkVideo = (file) => {
    try {
        if (file.type.startsWith('video/')) {
            imageOk = false;
            return true
        } else {
            return false
        }
    } catch {
        return false
    }
}



// //////////////////////////////////////////////////
// 기타
askInitMessage = (user_id) => {
    Swal.fire({
        html: `
<div class="mt-4">
    <!-- 제목 -->
    <div class="text-center pb-4">
        <h1 class="text-dark">알림 지우기</h1>
    </div>
    <!-- 내용 -->
    <diV class="text-start">
        <p class="text-secondary">
            알림센터에 있는 모든 알림을 지울까요?
        </p>
    </div>
</div>`,
        icon: 'warning',
        showConfirmButton: true,
        confirmButtonText: '지우기',
        showCancelButton: true,
        cancelButtonText: `취소`
    })
    .then(async (result) => {
        if (result.isConfirmed) {
            var messages = [];
            await getData({
                model: 'CHAT',
                id: '',
                field: 'to_id',
                value: user_id
            }).then((data) => messages = messages.concat(JSON.parse(data.db)));

            for(var i = 0; i < messages.length; i++) {
                await setData({
                    model: 'CHAT',
                    id: messages[i].pk,
                    field_value: JSON.stringify({
                        read: "y"
                    })
                })
            }

            document.location.reload();
        }
    });
}

// //////////////////////////////////////////////////
// ORMS
sortTable = (list, key, sign) => {
    try {
        return list.sort((a, b) => {
            let valA = a.fields[key];
            let valB = b.fields[key];

            console.log(`valA: ${valA}, valB: ${valB}`);

            // 문자열이 아닌 경우에는 다른 방법으로 비교
            if (typeof valA !== 'string' || typeof valB !== 'string') {
                if (sign === '+') {
                    return valA > valB ? 1 : valA < valB ? -1 : 0;
                } else if (sign === '-') {
                    return valA < valB ? 1 : valA > valB ? -1 : 0;
                }
            } else {
                // 문자열인 경우 localeCompare 사용
                if (sign === '+') {
                    return valA.localeCompare(valB);
                } else if (sign === '-') {
                    return valB.localeCompare(valA);
                }
            }
        });
    } catch (error) {
        console.error('An error occurred during sorting:', error);
        console.log('a:', a);
        console.log('b:', b);
        console.log('valA:', valA);
        console.log('valB:', valB);
        return list; // 에러 발생 시 원래 리스트를 반환
    }
}

async function uploadFile(file){
    var url = `/orm/upload_file`;
    var formData = new FormData();
    formData.append('file', file)
    var path = "";
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            path = data["path"];
        });
    return path
}

async function getData(options) {
    var model = options.model;
    var id = options.id;
    var field = options.field;
    var value = options.value;
    //검색조건들이 빈값일 경우, 검색조건 누락(<=Fun Cool Sexy??)
    var url = `/orm/data`;
    var output = ""
    await fetch(`${url}?model=${model}&id=${id}&field=${field}&value=${value}`, {
        method: 'GET'
    })
        .then((response) => response.json())
        .then((data) => {
            var success = data["success"];
            if (success == "y") {
                //var success = data.success;
                //var dbData = JSON.parse(data.db); // db 데이터를 JSON으로 파싱
                //var model = dbData[0].model;
                //var pk = dbData[0].pk;
                //var name = dbData[0].fields.name;
            
                // 아래에 가져온 데이터를 처리
                console.log(data.message);
                console.log(data.db);
                output = data;
            } else {
                console.log(data.message);
            }
        })
    return output
}

async function setData(options){
    var model = options.model;
    var id = options.id;//수정 시 작성(추가 시는 빈 값)
    var field_value = options.field_value;//업데이트 또는 생성할 필드명과 필드값을 Json 양식으로 작성할 것
    /*
    [field_value의 JSON 양식 예시]
    `
    {
        "name": "이름값",
        "affiliation_id": "소속값",
        "do_ids": "유저값",
        "charge_id_1": "유저값",
        "note": "메모값"
    }
    `
    */
    var url = `/orm/data`;
    var formData = new FormData();
    formData.append('model', model)
    formData.append('id', id)
    formData.append('field_value', field_value)
    var output = "";
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            var success = data["success"];
            if (success == "y") {
                console.log(data.message);
                console.log(data.db);
                output = data;
            } else {
                console.log(data.message);
                console.log(data)
            }
        })
    return output
}

function deleteData(options){
    var model = options.model;
    var id = options.id;
    var field = options.field;
    var value = options.value;
    var url = `/orm/data`;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`${url}?model=${model}&id=${id}&field=${field}&value=${value}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
        .then((response) => response.json())
        .then((data) => {
            var success = data["success"];
            if (success == "y") {
                console.log(data.message);
                console.log(data.db);
            } else {
                console.log(data.message);
                console.log(data);
            }
        })
}

//api로 접근이 가능한 모델(테이블)을 확인
function orm_doctor(){
    var url = `/orm/orm_doctor`;
    fetch(url, {method: 'GET'})
    .then(response => response.text())
    .then(data => {
        console.log(data); // 서버에서 받은 텍스트를 출력
    })
    .catch(error => {
        console.error('Error', error);
    });
};

// 페이레터
/*
pgcode: 결제수단 코드
creditcard	신용카드
banktransfer	인터넷뱅킹(금융결제원)
virtualaccount	가상계좌
mobile	휴대폰
voucher	문화상품권
book	도서상품권
culture	컬쳐랜드상품권
smartculture	스마트문상
happymoney	해피머니상품권
mobilepop	모바일팝
teencash	틴캐시
tmoney	교통카드결제
cvs	편의점캐시
eggmoney	에그머니
oncash	온캐시
phonebill	폰빌
cashbee	이즐
kakaopay	카카오페이
payco	페이코
checkpay	체크페이
toss	토스
ssgpay	SSG페이
naverpay	네이버페이
samsungpay	삼성페이
smilepay	스마일페이
applepay	애플페이
*/
TEST_URL = 'https://dev-api.payletter.com'
LIVE_URL = 'https://api.payletter.com'
// 페이레터 결제 요청
plRequestPurchase = async (pgcode, user_id, user_name, service_name, client_id, order_no, amount, taxfree_amount, tax_amount, product_name, email_flag, email_addr, autopay_flag, receipt_flag, custom_parameter, return_url, callback_url, cancel_url, key) => {
    var url = '/api/payment/request';
    url = '/v1.0/payments/request';
    fetch('https://testpgapi.payletter.com/v1.0/payments/request', {
        method: 'post',
        mode: 'no-cors',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=`
        },
        body: JSON.stringify({
            pgcode: pgcode, // 결제수단 코드(표 참고)
            client_id: client_id, // 가맹점 아이디
            service_name: service_name, // 결제 서비스 이름
            user_id: user_id, // 결제 유저 아이디
            user_name: user_name, // 결제 유저 이름
            order_no: order_no, // 주문번호(주문 아이디)
            amount: amount, // 결제 금액
            taxfree_amount: taxfree_amount, // 비과세 금액
            tax_amount: tax_amount, // 부가세 금액
            product_name: product_name, // 상품명
            email_flag: email_flag, // 결제 이메일 수신 여부(Y/N)
            email_addr: email_addr, // 결제 이메일 수신 주소(이메일 수신 여부가 Y일 경우 필수)
            autopay_flag: autopay_flag, // 자동결제 여부(Y/N)
            receipt_flag: receipt_flag, // 현금영수증 발급 여부(Y/N)
            custom_parameter: custom_parameter, // 사용자 정의 파라미터(결과 콜백으로 전달)
            return_url: return_url, // 결제 완료 후 이동할 URL
            callback_url: callback_url, // 결제 결과 콜백 URL
            cancel_url: cancel_url, // 결제 취소 URL
        })
    }).then((response) => {
        console.log(response);
        return response.json();
    }).then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var tid = data["tid"]; // 결제 아이디
            var cid = data["cid"]; // 승인번호
            var amount = data["amount"]; // 결제 금액
            var transaction_date = data["transaction_date"]; // 결제 일시(YYYY-MM-DD HH:MM:SS)
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 반복 결제 승인
plConfirmSubscribe = async (pgcode, user_id, user_name, service_name, client_id, order_no, amount, taxfree_amount, tax_amount, product_name, billkey, ip_addr, key) => {
    const url = 'testpgapi.payletter.com/v1.0/payments/autopay';
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
        body: JSON.stringify({
            pgcode: pgcode, // 결제수단 코드(표 참고)
            user_id: user_id, // 결제 유저 아이디
            user_name: user_name, // 결제 유저 이름
            service_name: service_name, // 결제 서비스 이름
            client_id: client_id, // 가맹점 아이디
            order_no: order_no, // 주문번호(주문 아이디)
            amount: amount, // 결제 금액
            taxfree_amount: taxfree_amount, // 비과세 금액
            tax_amount: tax_amount, // 부가세 금액
            product_name: product_name, // 상품명
            billkey: billkey, // 자동 재결제용 결제키
            ip_addr: ip_addr // 결제자 IP 주소
        })
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var tid = data["tid"]; // 결제 아이디
            var cid = data["cid"]; // 승인번호
            var amount = data["amount"]; // 결제 금액
            var transaction_date = data["transaction_date"]; // 결제 일시(YYYY-MM-DD HH:MM:SS)
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 결제 취소
plCancelPurchase = async (pgcode, client_id, user_id, tid, ip_addr, key) => {
    const url = 'testpgapi.payletter.com/v1.0/payments/cancel';
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
        body: JSON.stringify({
            pgcode: pgcode, // 결제수단 코드(표 참고)
            client_id: client_id, // 가맹점 아이디
            user_id: user_id, // 결제 유저 아이디
            tid: tid, // 결제 아이디
            ip_addr: ip_addr // 결제자 IP 주소
        })
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var tid = data["tid"]; // 결제 아이디
            var cid = data["cid"]; // 승인번호
            var amount = data["amount"]; // 결제 금액
            var cancel_date = data["cancel_date"]; // 취소 일시(YYYY-MM-DD HH:MM:SS)
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 일부 결제 취소
plPartialCancelPurchase = async (pgcode, client_id, user_id, tid, amount, taxfree_amount, tax_amount, ip_addr, key) => {
    const url = 'testpgapi.payletter.com/v1.0/payments/cancel/partial';
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
        body: JSON.stringify({
            pgcode: pgcode, // 결제수단 코드(표 참고)
            client_id: client_id, // 가맹점 아이디
            user_id: user_id, // 결제 유저 아이디
            tid: tid, // 결제 아이디
            amount: amount, // 취소 금액
            taxfree_amount: taxfree_amount, // 비과세 금액
            tax_amount: tax_amount, // 부가세 금액
            ip_addr: ip_addr // 결제자 IP 주소
        })
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var tid = data["tid"]; // 결제 아이디
            var cid = data["cid"]; // 승인번호
            var amount = data["amount"]; // 결제 금액
            var cancel_date = data["cancel_date"]; // 취소 일시(YYYY-MM-DD HH:MM:SS)
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 결제 로그 조회
purchaseLog = async (client_id, date, date_type, pgcode, key) => {
    // client_id: 가맹점 아이디
    // date: 조회 일자(YYYYMMDD)
    // date_type: 조회 일자 타입(transaction-처음결제일, settle-결제 완료 또는 취소일)
    // pgcode: 결제수단 코드(표 참고)
    var url = 'testpgapi.payletter.com/v1.0/payments/transaction/list';
    url = `${url}?client_id=${client_id}&date=${date}&date_type=${date_type}&pgcode=${pgcode}`;
    await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var total_count = data["total_count"];
            var logs = data["list"];
            for (var i = 0; i < logs.length; i++) {
                var pgcode = logs[i]["pgcode"]; // 결제수단 코드
                var user_id = logs[i]["user_id"]; // 결제 유저 아이디
                var user_name = logs[i]["user_name"]; // 결제 유저 이름
                var tid = logs[i]["tid"]; // 결제 아이디
                var cid = logs[i]["cid"]; // 승인번호
                var amount = logs[i]["amount"]; // 결제 금액
                var taxfree_amount = logs[i]["taxfree_amount"]; // 비과세 금액
                var tax_amount = logs[i]["tax_amount"]; // 부가세 금액
                var order_no = logs[i]["order_no"]; // 주문번호(주문 아이디)
                var product_name = logs[i]["product_name"]; // 상품명
                var status_code = logs[i]["status_code"]; // 결제 상태 코드
                var transaction_date = logs[i]["transaction_date"]; // 결제 일시(YYYY-MM-DD HH:MM:SS)
                var cancel_date = logs[i]["cancel_date"]; // 취소 일시(YYYY-MM-DD HH:MM:SS)
            }
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 현금영수증 발급
writeCashReceipt = async (client_id, type, tax_flag, return_url, tid, key) => {
    // tid: 결제 아이디
    var url = `testpgapi.payletter.com/v1.0/cashreceipt/issue/${tid}`;
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
        body: JSON.stringify({
            client_id: client_id, // 가맹점 아이디
            type: type, // 용도(0-사용자가 선택, 1-소득공제용, 2-지출증빙용)
            tax_flag: tax_flag, // 부가세 포함 여부(Y/N)
            return_url: return_url, // 현금영수증 발급 완료 후 이동할 URL
        })
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var receipt_url = data["receipt_url"]; // 현금영수증 발급 URL
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 결제 상태 조회
purchaseStatus = async (client_id, order_no, key) => {
    var url = `testpgapi.payletter.com/v1.0/payments/status`;
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
        body: JSON.stringify({
            client_id: client_id, // 가맹점 아이디
            order_no: order_no, // 주문번호(주문 아이디)
        })
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var code = data["code"]; // 결제 상태 코드
            var message = data["message"]; // 결제 상태 메세지
            var client_id = data["client_id"]; // 가맹점 아이디
            var order_no = data["order_no"]; // 주문번호(주문 아이디)
            var token = data["token"]; // 결제 인증 토큰
            var tid = data["tid"]; // 결제 아이디
            var status_code = data["status_code"]; // 결제 상태 코드(1-생성, 2-확인, 3-인증, 4-취소됨, 5-완료됨)
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

// 페이레터 결제 확인
getRecipt = async (tid, key) => {
    // tid: 결제 아이디
    var url = `testpgapi.payletter.com/v1.0/recipt/info/${tid}`;
    await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA=${key}`
        },
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

        if (data.status_code == 200) {
            var receipt_url = data["receipt_url"]; // 영수증 URL
        } else {
            var code = data["code"]; // 오류 코드
            var message = data["message"]; // 오류 메세지
        }
    });
}

function checkUserAgent() {
    const userAgent = navigator.userAgent.toLowerCase();

    if (userAgent.includes('windows') || userAgent.includes('macintosh') || userAgent.includes('linux')) {
        return 'pc'; // PC
    } else if (userAgent.includes('android')) {
        return 'aos'; // Android OS
    } else if (userAgent.includes('iphone') || userAgent.includes('ipad') || userAgent.includes('ipod')) {
        return 'ios'; // iOS (iPhone, iPad, iPod)
    } else {
        return 'unknown'; // 그 외
    }
}

deleteTableData = async (model, id) => {
    Swal.fire({
        html: `
        <div>
            <div class="text-center py-4">
                <h1 class="text-dark">삭제 확인</h1>
            </div>
            <diV class="text-start">
                <p class="text-secondary">
                    선택하신 데이터를 정말 삭제하시겠습니까?
                </p>
            </div>
        </div>`,
        icon: `warning`,
        showConfirmButton: true,
        confirmButtonText: `삭제하기`,
        confirmButtonColor: `#dc3545`,
        showCancelButton: true,
        cancelButtonText: `취소`,
    }).then(async (result) => {
        if (result.isConfirmed) {
            await deleteData({
                model: model,
                id: id
            });
            window.location.reload();
        }
    });
}
