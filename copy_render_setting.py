import c4d
from c4d import documents, gui, storage
import os

class CustomDialog(gui.GeDialog):
    BASE_FILE_ID = 1000
    TARGET_DIR_ID = 1001
    BASE_BTN_ID = 1003
    TARGET_BTN_ID = 1004
    START_BTN_ID = 1002
    REMOVE_EXISTING_ID = 1005

    def CreateLayout(self):
        self.SetTitle("Copy Render Settings")

        # Base file selection
        self.AddStaticText(self.BASE_FILE_ID + 10, c4d.BFH_LEFT, name="Base .c4d file:")
        self.AddEditText(self.BASE_FILE_ID, c4d.BFH_SCALEFIT)
        self.AddButton(self.BASE_BTN_ID, c4d.BFH_LEFT, name="...")

        # Target folder selection
        self.AddStaticText(self.TARGET_DIR_ID + 10, c4d.BFH_LEFT, name="Target Folder:")
        self.AddEditText(self.TARGET_DIR_ID, c4d.BFH_SCALEFIT)
        self.AddButton(self.TARGET_BTN_ID, c4d.BFH_LEFT, name="...")

        # Option to remove existing render settings
        self.AddCheckbox(self.REMOVE_EXISTING_ID, c4d.BFH_LEFT, initw=100, inith=15, name="Remove existing render settings")

        self.AddButton(self.START_BTN_ID, c4d.BFH_CENTER, name="Start Copying")

        return True

    def Command(self, id, msg):
        if id == self.START_BTN_ID:
            base_file = self.GetString(self.BASE_FILE_ID)
            target_folder = self.GetString(self.TARGET_DIR_ID)
            remove_option = self.GetBool(self.REMOVE_EXISTING_ID)
            copy_render_settings_from_dialog(base_file, target_folder, remove_option)
            gui.MessageDialog('Copying Completed!')
            self.Close()
        elif id == self.BASE_BTN_ID:
            filepath = c4d.storage.LoadDialog(title="Select Base .c4d file", flags=c4d.FILESELECT_LOAD, force_suffix="c4d")
            if filepath:
                self.SetString(self.BASE_FILE_ID, filepath)
        elif id == self.TARGET_BTN_ID:
            dirpath = c4d.storage.LoadDialog(title="Select Target Folder", flags=c4d.FILESELECT_DIRECTORY)
            if dirpath:
                self.SetString(self.TARGET_DIR_ID, dirpath)

        return True

def copy_all_render_settings(source_doc, target_doc, remove_existing=True):
    # Only remove if checkbox is checked
    if remove_existing:
        render_data_head = target_doc.GetFirstRenderData()
        while render_data_head:
            next_render_data = render_data_head.GetNext()
            render_data_head.Remove()
            render_data_head = next_render_data

    # Copy all render settings
    source_render_data = source_doc.GetFirstRenderData()
    while source_render_data:
        cloned_data = source_render_data.GetClone()
        target_doc.InsertRenderData(cloned_data)
        source_render_data = source_render_data.GetNext()

def copy_render_settings_from_dialog(base_file, target_folder, remove_existing=True):
    base_doc = documents.LoadDocument(base_file, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
    if not base_doc:
        print("Base file could not be loaded!")
        return

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith(".c4d"):
                file_path = os.path.join(root, file)
                doc = documents.LoadDocument(file_path, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
                if not doc:
                    print(f"Failed to load {file_path}")
                    continue

                copy_all_render_settings(base_doc, doc, remove_existing)
                documents.SaveDocument(doc, file_path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)
    c4d.EventAdd()

if __name__=='__main__':
    dialog = CustomDialog()
    dialog.Open(dlgtype=c4d.DLG_TYPE_MODAL, defaultw=400, defaulth=150)
