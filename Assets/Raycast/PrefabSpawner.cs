using UnityEngine;

public class PrefabSpawner : MonoBehaviour
{
    public GameObject prefab; // Assign your prefab in the inspector

    public void SpawnPrefabWithString(string textToShow)
    {
        GameObject instance = Instantiate(prefab, transform.position, Quaternion.identity);
        TextDisplay display = instance.GetComponent<TextDisplay>();
        if (display != null)
            display.SetText(textToShow);
        else
            Debug.LogError("TextDisplay script not found on prefab.");
    }
}
