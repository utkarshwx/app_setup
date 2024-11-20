'use client'

import { useState, useRef } from 'react'
import { Upload, Video } from 'lucide-react'

export default function Component() {
  const [file, setFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [videoPreviewUrl, setVideoPreviewUrl] = useState<string | null>(null)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile && selectedFile.type.startsWith('video/')) {
      setFile(selectedFile)
      setVideoPreviewUrl(URL.createObjectURL(selectedFile))

    } else {
      alert('Please select a valid video file.')
    }
  }

  const simulateUpload = () => {
    setUploadProgress(0)
    handleUpload()
    const interval = setInterval(() => {
      setUploadProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(interval)
          return 100
        }
        return prevProgress + 10
      })
    }, 500)
  }

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      setUploadProgress(0);
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("File upload failed");
      }

      const result = await response.json();
      setDownloadUrl(result.downloadUrl);

      // Simulate upload progress for user feedback
      const interval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + 10;
        });
      }, 200);
    } catch (error) {
      alert(`Error uploading file: `);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Video Upload</h1>
        </div>
      </header>
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Video Upload</h2>
          <div className="space-y-4">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="video/*"
              className="hidden"
              aria-label="Select video file"
            />
            <button
              className="w-full bg-white hover:bg-black text-black hover:text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center justify-center transition duration-150 ease-in-out"
              onClick={() => fileInputRef.current?.click()}
            >
              <Video className="mr-2 h-5 w-5" />
              Select Video
            </button>
            {file && (
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  Selected video: {file.name}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 mb-4">
                  <div
                    className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${uploadProgress}%` }}
                    role="progressbar"
                    aria-valuenow={uploadProgress}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  ></div>
                </div>
                {videoPreviewUrl && (
                  <video
                    src={videoPreviewUrl}
                    controls
                    className="w-full max-h-64 object-contain bg-black mb-4"
                  >
                    Your browser does not support the video tag.
                  </video>
                )}
                <button
                  className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center justify-center transition duration-150 ease-in-out"
                  onClick={simulateUpload}
                >
                  <Upload className="mr-2 h-5 w-5" />
                  Upload Video
                </button>
              </div>
            )}
            {downloadUrl && (
              <div className="mt-4">
                <a
                  href={downloadUrl}
                  className="w-full bg-white hover:bg-black text-black hover:text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center justify-center transition duration-150 ease-in-out"
                  download
                >
                  Download Processed Video
                </a>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}