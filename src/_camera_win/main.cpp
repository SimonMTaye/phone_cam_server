
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Windows.h>

namespace py = pybind11;

HANDLE fileHandle = NULL;
LPCSTR mutexName = "Global\\PlayoutXVCammutex";
LPCSTR fileHandleName = "PlayoutXVCam";

uint8_t *processIntoFrame(uint8_t *data, int pixelnum)
{
    int bufSize = pixelnum * 4;
    uint8_t *frame = (uint8_t *)malloc(bufSize);
    CopyMemory(frame, data, bufSize);
    for (size_t i = 0; i < pixelnum; i++)
    {
        uint8_t r = frame[i * 4];
        uint8_t b = frame[(i * 4) + 2];
        frame[i * 4] = b;
        frame[(i * 4) + 2] = r;
    }
    return frame;
}

int sendFrame(long frameIndex, int fps, int width, int height, py::array_t<uint8_t, py::array::c_style> data)
{
    py::buffer_info buf = data.request();
    if (buf.ndim != 3 || buf.shape[2] != 4)
    {
        throw std::runtime_error("Given data doesn't represent a well-formed frame");
    }

    uint8_t *frame = processIntoFrame((uint8_t *)buf.ptr, width * height);
    int bufferSize = width * height * 4;
    int fileSize = (sizeof(int) * 4) + sizeof(long) + bufferSize;
    LARGE_INTEGER memSize;
    memSize.QuadPart = fileSize;

    // Access the FileMapping Object to share data with the DirecShow filter
    if (fileHandle == NULL)
    {
        fileHandle = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, memSize.HighPart, memSize.LowPart, fileHandleName);
    }

    if (fileHandle == NULL)
    {
        return GetLastError();
    }
    // Used to synchronize access of FileMapping Object with the DirectShow filter
    HANDLE fileMutex = CreateMutex(NULL, FALSE, mutexName);
    if (fileMutex == NULL)
    {
        return GetLastError();
    }
    // Wait untill mutex is released, signalling that it is okay to modify the file mapping
    WaitForSingleObject(fileMutex, 1000);

    // Get a pointer to the shared memmory and copy the image
    void *fileView = MapViewOfFile(fileHandle, FILE_MAP_ALL_ACCESS, 0, 0, 0);
    CopyMemory(fileView, &frameIndex, sizeof(long));
    CopyMemory((byte *)fileView + 8, &fps, sizeof(int));
    CopyMemory((byte *)fileView + 12, &width, sizeof(int));
    CopyMemory((byte *)fileView + 16, &height, sizeof(int));
    CopyMemory((byte *)fileView + 20, &bufferSize, sizeof(int));
    CopyMemory((byte *)fileView + 24, frame, bufferSize);

    FlushViewOfFile(fileView, fileSize);
    UnmapViewOfFile(fileView);

    ReleaseMutex(fileMutex);
    CloseHandle(fileMutex);
    free(frame);

    return 0;
}

void closeCamera()
{
    if (fileHandle != NULL)
    {
        CloseHandle(fileHandle);
    }
}

PYBIND11_MODULE(camera_win, m)
{
    m.doc() = "Send data to the virtual camera using c++";
    m.def("send", &sendFrame, "Send a frame to the camera");
    m.def("close", &closeCamera, "Release resources used to transfer data to the camera");
}