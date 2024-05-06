using TMPro;
using UnityEngine;

public class TextDisplay : MonoBehaviour
{
    public TextMeshProUGUI textMesh;

    private void Awake()
    {
        textMesh = GetComponent<TextMeshProUGUI>();
    }

    public void SetText(string text)
    {
        if (textMesh != null)
            textMesh.text = text;
        else
            Debug.LogError("No TextMeshPro component found.");
    }
}
