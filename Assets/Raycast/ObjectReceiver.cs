using System;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class ObjectReceiver : MonoBehaviour
{
    public AutoRayCast autoRayCast; // Reference to the AutoRayCast script

    TcpClient client;
    NetworkStream stream;
    StringBuilder messageBuffer = new StringBuilder();

    void Start()
    {
        try
        {
            client = new TcpClient("192.168.1.112", 12345);
            stream = client.GetStream();
        }
        catch (Exception ex)
        {
            Debug.LogError("Failed to connect: " + ex.Message);
        }
    }

    void Update()
    {
        try
        {
            if (stream != null && stream.DataAvailable)
            {
                byte[] data = new byte[1024];
                int bytes = stream.Read(data, 0, data.Length);
                messageBuffer.Append(Encoding.UTF8.GetString(data, 0, bytes));

                // Check for complete messages in the buffer
                string bufferContent = messageBuffer.ToString();
                int delimiterIndex = bufferContent.IndexOf('\n');
                while (delimiterIndex != -1)
                {
                    string message = bufferContent.Substring(0, delimiterIndex).Trim();
                    ProcessData(message);
                    bufferContent = bufferContent.Substring(delimiterIndex + 1);
                    delimiterIndex = bufferContent.IndexOf('\n');
                }
                messageBuffer.Clear();
                messageBuffer.Append(bufferContent);
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("Error reading from network stream: " + ex.Message);
        }
    }

    void ProcessData(string data)
    {
        try
        {
            // Assume data format "centerX,centerY,class\n"
            var coordinates = data.Split(',');
            if (coordinates.Length == 3)
            {
                float centerX = float.Parse(coordinates[0]);
                float centerY = float.Parse(coordinates[1]);
                string objClass = coordinates[2];
                autoRayCast.RaycastFromYOLO(centerX, centerY, objClass);
            }
        }
        catch (FormatException ex)
        {
            Debug.LogError("Format error: " + ex.Message);
        }
        catch (Exception ex)
        {
            Debug.LogError("Processing error: " + ex.Message);
        }
    }

    void OnDestroy()
    {
        if (stream != null)
        {
            stream.Close();
        }
        if (client != null)
        {
            client.Close();
        }
    }
}
