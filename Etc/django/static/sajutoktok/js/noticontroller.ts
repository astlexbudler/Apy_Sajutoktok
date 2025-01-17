import express   from 'express';

const router = express.Router({ caseSensitive: true });

/*----------------------------------------
Json 응답
----------------------------------------*/
const jsonResult = {
    withoutData: (code: any, message: any) => {
        return jsonResult.combine(code, message, null);
    },
    withData: (code: any, message: any, data: any) => {
        return jsonResult.combine(code, message, data);
    },
    combine: (code: any, message: any, data: any) => {
        const result = {
            code: code,
            message: message
        };

        if (!data) {
            return result;
        } else {
            return {
                ...result,
                data: data
            };
        }
    }
};

const noti = {
    /*----------------------------------------
    Noti Process
    ----------------------------------------*/
    payProcess: async(req: any, res: any, next: any)=> {
        // Call back URL 로 결제결과 유입
        // Call back 데이터를 통해 결과값을 받아 가맹점에 맞는 충전구매 등의 로직을 수행합니다.
        if (req.body.constructor === Object && Object.keys(req.body).length == 0){
            res.json(
                // code 가 0이 아닌 경우에는 통보가 실패한 것으로 간주되어 5분마다 최대 20번까지 재 전송됩니다.
                jsonResult.withoutData(9999, 'data is empty')
            )
        }
        else{
        //-----------------------------------------------------------------------------------------
        // Description : 결제 결과 정보 세팅
        //              - 고객사에서 아래 결제 정보를 DB에 저장해 놓으시면 됩니다. 
        //              - 아래 정보들을 디버깅성으로 파일로그를 남겨놓으시기를 권고 드립니다.
        //              - Return Url / CallBack Url로 전달된 파라메터는 위/변조 방지를 위하여 SHA256 hash 값을 생성한 후 전달된 payhash 와 비교 검증을 수행하시기 바랍니다.
        //              - CallBack URL에서 처리 완료 후 성공시 {"code":0, "message":"실패시 실패 사유"} 형태의 json 문자열을 출력해 주시기 바랍니다.
        //              - code 가 0이 아닌 경우에는 통보가 실패한 것으로 간주되어 5분마다 최대 20번까지 재 전송됩니다.
        //-----------------------------------------------------------------------------------------

        // Sample Data - 정확한 값은 문서를 참고하시기 바랍니다.
        // req.body.user_id          : 결제자 아이디
        // req.body.user_name        : 결제자 명
        // req.body.order_no         : 결제 주문번호
        // req.body.service_name     : 서비스 명
        // req.body.product_name     : 상품명
        // req.body.custom_parameter : 주문요청시 가맹점이 전송한 값
        // req.body.tid              : 결제고유번호
        // req.body.cid              : 승인번호
        // req.body.amount           : 결제요청금액
        // req.body.pay_info         : 결제 부가정보
        // req.body.pgcode           : 결제요청한 pg명
        // req.body.billkey          : 자동결제 재결제용 빌키
        // req.body.domestic_flag    : 국내/ 해외 신용카드 구분 (Y : 국내, N : 해외)
        // req.body.transaction_date : 거래일시 (yyyy-MM-dd hh:mm:ss)
        // req.body.card_info        : 카드번호 (중간 4자리 masking)
        // req.body.payhash          : 파라미터 검증을 위한 SHA256 hash 값 (user_id+amount+tid+결제용 API KEY) 일부결제수단은 전달되지않음 (가상계좌)

        // req.body.cash_receipt.cid        : 현금영수증 CID
        // req.body.cash_receipt.code       : 현금영수증 Code
        // req.body.cash_receipt.deal_no    : 현금영수증 Deal No
        // req.body.cash_receipt.issue_type : 현금영수증 Issue Type
        // req.body.cash_receipt.message    : 현금영수증 Message
        // req.body.cash_receipt.payer_sid  : 현금영수증 Payer SID
        // req.body.cash_receipt.type       : 현금영수증 Type

            // Json 값 외에 html 및 다른 코드가 해당페이지에 노출되지 않도록 합니다.
            // 성공시 코드값 : 0, 실패시 0이 아닌 최대 4자리 숫자
            jsonResult.withoutData(0, 'success')
        }
    }
};
router.post('/Noti', noti.payProcess);
export default { noti }