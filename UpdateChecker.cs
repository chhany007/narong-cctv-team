using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Diagnostics;
using System.IO;
using Newtonsoft.Json;

namespace IP
{
    public class UpdateInfo
    {
        public string Version { get; set; }
        public string DownloadUrl { get; set; }
        public string ReleaseNotes { get; set; }
        public DateTime ReleaseDate { get; set; }
    }

    public class UpdateChecker
    {
        private const string UPDATE_CHECK_URL = "https://your-server.com/api/version.json";
        private static readonly string CurrentVersion = "1.0.0"; // Update this with your current version
        
        public static async Task<UpdateInfo> CheckForUpdatesAsync()
        {
            try
            {
                using (var client = new HttpClient())
                {
                    client.Timeout = TimeSpan.FromSeconds(10);
                    var response = await client.GetStringAsync(UPDATE_CHECK_URL);
                    var updateInfo = JsonConvert.DeserializeObject<UpdateInfo>(response);
                    
                    if (IsNewerVersion(updateInfo.Version, CurrentVersion))
                    {
                        return updateInfo;
                    }
                }
            }
            catch (Exception ex)
            {
                // Log error silently
                Debug.WriteLine($"Update check failed: {ex.Message}");
            }
            
            return null;
        }
        
        private static bool IsNewerVersion(string newVersion, string currentVersion)
        {
            try
            {
                var newVer = new Version(newVersion);
                var curVer = new Version(currentVersion);
                return newVer > curVer;
            }
            catch
            {
                return false;
            }
        }
        
        public static async Task<string> DownloadUpdateAsync(string downloadUrl, IProgress<int> progress)
        {
            try
            {
                var tempPath = Path.Combine(Path.GetTempPath(), "setup.exe");
                
                using (var client = new HttpClient())
                {
                    using (var response = await client.GetAsync(downloadUrl, HttpCompletionOption.ResponseHeadersRead))
                    {
                        response.EnsureSuccessStatusCode();
                        var totalBytes = response.Content.Headers.ContentLength ?? -1L;
                        
                        using (var contentStream = await response.Content.ReadAsStreamAsync())
                        using (var fileStream = new FileStream(tempPath, FileMode.Create, FileAccess.Write, FileShare.None))
                        {
                            var buffer = new byte[8192];
                            long totalRead = 0;
                            int bytesRead;
                            
                            while ((bytesRead = await contentStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                            {
                                await fileStream.WriteAsync(buffer, 0, bytesRead);
                                totalRead += bytesRead;
                                
                                if (totalBytes > 0)
                                {
                                    progress?.Report((int)((totalRead * 100) / totalBytes));
                                }
                            }
                        }
                    }
                }
                
                return tempPath;
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to download update: {ex.Message}");
            }
        }
        
        public static void InstallUpdate(string installerPath)
        {
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = installerPath,
                    UseShellExecute = true,
                    Verb = "runas" // Run as administrator
                });
                
                Application.Exit();
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to start installer: {ex.Message}");
            }
        }
    }
}
