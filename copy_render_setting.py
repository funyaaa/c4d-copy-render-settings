import c4d
from c4d import documents, storage, gui
import os

def copy_all_render_settings(source_doc, target_doc):
    # 既存のレンダリング設定を削除
    render_data_head = target_doc.GetFirstRenderData()
    while render_data_head:
        next_render_data = render_data_head.GetNext()
        render_data_head.Remove()
        render_data_head = next_render_data

    # 全てのレンダリング設定をコピー
    source_render_data = source_doc.GetFirstRenderData()
    while source_render_data:
        cloned_data = source_render_data.GetClone()
        target_doc.InsertRenderData(cloned_data)
        source_render_data = source_render_data.GetNext()

def main():
    base_file = f""  # ベースの.c4dファイルのパスを設定
    target_folder = f""   # 変更したい.c4dファイルがあるフォルダのパスを設定
    # ベースファイルを開く
    base_doc = documents.LoadDocument(base_file, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
    if not base_doc:
        print("Base file could not be loaded!")
        return

    # 指定したフォルダの.c4dファイルすべてに対して処理
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith(".c4d"):
                file_path = os.path.join(root, file)

                # ファイルを開く
                doc = documents.LoadDocument(file_path, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
                if not doc:
                    print(f"Failed to load {file_path}")
                    continue

                # レンダリング設定をコピー
                copy_all_render_settings(base_doc, doc)

                # 変更を保存
                documents.SaveDocument(doc, file_path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT)

    c4d.EventAdd()

    # 処理完了のアラートを表示
    gui.MessageDialog('All render settings have been copied successfully!')

if __name__=='__main__':
    main()
