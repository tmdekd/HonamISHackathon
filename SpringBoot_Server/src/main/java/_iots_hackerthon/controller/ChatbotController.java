package _iots_hackerthon.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;

import java.util.Map;

@Controller
public class ChatbotController {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String FASTAPI_URL = "http://127.0.0.1:8000/api/chatbot/";

    // HTML 페이지 반환
    @GetMapping("/chat")
    public String chatPage() {
        return "chat.html"; // src/main/resources/templates/chat.html
    }

    @GetMapping("/chat2")
    public String chat2Page() {
        return "chat2.html"; // src/main/resources/templates/chat2.html
    }

    // 프론트에서 Ajax 요청 들어오면 → FastAPI 호출 → 응답 리턴 + MongoDB 저장
    @PostMapping("/api/chatbot")
    @ResponseBody
    public Map<String, Object> chat(@RequestBody Map<String, String> payload) {
        ResponseEntity<Map<String, Object>> responseEntity = restTemplate.exchange(
                "http://127.0.0.1:8000/api/chatbot/",
                HttpMethod.POST,
                new org.springframework.http.HttpEntity<>(payload),
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        return responseEntity.getBody(); // 이제 반환 가능
    }


}