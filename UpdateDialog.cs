using System;
using System.Windows.Forms;
using System.Threading.Tasks;

namespace IP
{
    public partial class UpdateDialog : Form
    {
        private UpdateInfo updateInfo;
        
        public UpdateDialog(UpdateInfo info)
        {
            InitializeComponent();
            this.updateInfo = info;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.StartPosition = FormStartPosition.CenterParent;
            
            lblVersion.Text = $"Version {info.Version} is available!";
            txtReleaseNotes.Text = info.ReleaseNotes;
            progressBar.Visible = false;
        }
        
        private void InitializeComponent()
        {
            this.lblVersion = new Label();
            this.txtReleaseNotes = new TextBox();
            this.btnUpdate = new Button();
            this.btnLater = new Button();
            this.progressBar = new ProgressBar();
            this.lblProgress = new Label();
            
            this.SuspendLayout();
            
            // lblVersion
            this.lblVersion.AutoSize = true;
            this.lblVersion.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold);
            this.lblVersion.Location = new System.Drawing.Point(20, 20);
            
            // txtReleaseNotes
            this.txtReleaseNotes.Location = new System.Drawing.Point(20, 50);
            this.txtReleaseNotes.Multiline = true;
            this.txtReleaseNotes.ReadOnly = true;
            this.txtReleaseNotes.ScrollBars = ScrollBars.Vertical;
            this.txtReleaseNotes.Size = new System.Drawing.Size(440, 150);
            
            // progressBar
            this.progressBar.Location = new System.Drawing.Point(20, 210);
            this.progressBar.Size = new System.Drawing.Size(440, 23);
            
            // lblProgress
            this.lblProgress.Location = new System.Drawing.Point(20, 236);
            this.lblProgress.Size = new System.Drawing.Size(440, 20);
            this.lblProgress.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            
            // btnUpdate
            this.btnUpdate.Location = new System.Drawing.Point(280, 260);
            this.btnUpdate.Size = new System.Drawing.Size(90, 30);
            this.btnUpdate.Text = "Update Now";
            this.btnUpdate.Click += BtnUpdate_Click;
            
            // btnLater
            this.btnLater.Location = new System.Drawing.Point(370, 260);
            this.btnLater.Size = new System.Drawing.Size(90, 30);
            this.btnLater.Text = "Later";
            this.btnLater.Click += (s, e) => this.Close();
            
            // UpdateDialog
            this.ClientSize = new System.Drawing.Size(480, 310);
            this.Controls.Add(this.lblVersion);
            this.Controls.Add(this.txtReleaseNotes);
            this.Controls.Add(this.progressBar);
            this.Controls.Add(this.lblProgress);
            this.Controls.Add(this.btnUpdate);
            this.Controls.Add(this.btnLater);
            this.Text = "Update Available";
            
            this.ResumeLayout(false);
        }
        
        private Label lblVersion;
        private TextBox txtReleaseNotes;
        private Button btnUpdate;
        private Button btnLater;
        private ProgressBar progressBar;
        private Label lblProgress;
        
        private async void BtnUpdate_Click(object sender, EventArgs e)
        {
            btnUpdate.Enabled = false;
            btnLater.Enabled = false;
            progressBar.Visible = true;
            lblProgress.Visible = true;
            
            try
            {
                var progress = new Progress<int>(percent =>
                {
                    progressBar.Value = percent;
                    lblProgress.Text = $"Downloading... {percent}%";
                });
                
                lblProgress.Text = "Downloading update...";
                var installerPath = await UpdateChecker.DownloadUpdateAsync(updateInfo.DownloadUrl, progress);
                
                lblProgress.Text = "Starting installer...";
                UpdateChecker.InstallUpdate(installerPath);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Update failed: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                btnUpdate.Enabled = true;
                btnLater.Enabled = true;
                progressBar.Visible = false;
                lblProgress.Visible = false;
            }
        }
    }
}
