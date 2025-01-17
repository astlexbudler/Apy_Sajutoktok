import statusCode from 'http-status-codes';
import express    from 'express';
import axios      from 'axios';


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

const call = {
    /*----------------------------------------
    Call POQ API
    ----------------------------------------*/
    payRequest: async(req: any, res: any, next: any)=> {

        axios({
            method: "post", // 요청 방식
            url: "https://testpgapi.payletter.com/v1.0/payments/request", // 요청 주소
            headers : {
                Authorization : "PLKEY MTFBNTAzNTEwNDAxQUIyMjlCQzgwNTg1MkU4MkZENDA="
            },
            data: {
                "pgcode" : "mobile",
                "user_id":"test_user_id",
                "user_name":"테스터",    
                "service_name":"페이레터",    
                "client_id":"pay_test",
                "order_no":"1234567890",
                "amount":1000,
                "taxfree_amount": 100,
                "tax_amount": 20,
                "product_name":"테스트상품",    
                "email_flag":"Y",
                "email_addr":"payletter@payletter.com",
                "autopay_flag":"N",    
                "receipt_flag":"Y",
                "custom_parameter":"this is custom parameter",    
                "return_url":"https://testpg.payletter.com/result",
                "callback_url":"https://testpg.payletter.com/callback",
                "cancel_url":"https://testpg.payletter.com/cancel"
            }// 제공 데이터(body)
          }).catch(function (err: any){
            res.status(err.status || statusCode.INTERNAL_SERVER_ERROR);
            res.json(
                jsonResult.withoutData(process.env.FAIL_CODE, err.message)
            );
          }).then(function(response :any){
            console.log(response);
            res.json(
                jsonResult.withData(
                    process.env.SUCCESS_CODE,
                    process.env.SUCCESS_CODE_MSG,
                    response.data
                )
            );
          });
    }
};
router.get('/CallPOQAPI', call.payRequest);
export default { call }