package com.example.rest_service.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController

public class GreetingController {
    @GetMapping("/hello-world")
    public String hello() {
        return "Hello World!";
    }

}
