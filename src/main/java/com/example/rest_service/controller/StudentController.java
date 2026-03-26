package com.example.rest_service.controller;

import com.example.rest_service.entity.Student;
import com.example.rest_service.exception.BadRequestException;
import com.example.rest_service.service.StudentService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
public class StudentController {
    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @PostMapping("/students")
    public ResponseEntity<?> createStudents(@RequestBody List<Student> newStudents) {
        try {
            List<Student> updatedList = studentService.addStudents(newStudents);
            return ResponseEntity
                    .status(HttpStatus.OK)
                    .header("Content-Type", "application/json")
                    .body(updatedList);
        } catch (BadRequestException e) {
            return ResponseEntity
                    .status(HttpStatus.BAD_REQUEST)
                    .header("Content-Type", "text/plain")
                    .body(e.getMessage());
        }
    }
}
