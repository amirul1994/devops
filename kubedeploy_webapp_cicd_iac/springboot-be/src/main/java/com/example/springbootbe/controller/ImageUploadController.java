package com.example.springbootbe.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://react-fe:3000") // Removed allowCredentials
public class ImageUploadController {

    private static final String UPLOAD_DIR = "/var/www/uploads/images/";

    // Handle image upload
    @PostMapping("/upload-image")
    public ResponseEntity<String> uploadImage(@RequestParam("image") MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return ResponseEntity.badRequest().body("Please select a file to upload.");
        }

        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null || originalFilename.isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid file name.");
        }

        try {
            File uploadDir = new File(UPLOAD_DIR);
            if (!uploadDir.exists()) {
                uploadDir.mkdirs();
            }

            Path filePath = Paths.get(UPLOAD_DIR + originalFilename);
            Files.write(filePath, file.getBytes());

            return ResponseEntity.ok("Image uploaded successfully!");
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("Failed to upload image.");
        }
    }

    // Handle image update
    @PutMapping("/update-image")
    public ResponseEntity<String> updateImage(@RequestParam("image") MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return ResponseEntity.badRequest().body("Please select a file to update.");
        }

        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null || originalFilename.isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid file name.");
        }

        try {
            File uploadDir = new File(UPLOAD_DIR);
            if (!uploadDir.exists()) {
                uploadDir.mkdirs();
            }

            Path filePath = Paths.get(UPLOAD_DIR + originalFilename);

            // Delete the existing file if it exists
            if (Files.exists(filePath)) {
                Files.delete(filePath);
            }

            // Save the new file
            Files.write(filePath, file.getBytes());

            return ResponseEntity.ok("Image updated successfully!");
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("Failed to update image.");
        }
    }

    // Handle preflight requests
    @RequestMapping(value = {"/upload-image", "/update-image"}, method = RequestMethod.OPTIONS)
    public ResponseEntity<?> handleOptions() {
        return ResponseEntity.ok().build();
    }
}