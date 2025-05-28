실행 순서

우선 모든 가상환경 deactivate하기

`deactivate` or `conda deactivate`

`pip install uv`

`uv venv --python=3.9.19`

`source .venv/bin/activate` (Linux/macOS) / `.venv\Scripts\activate` (Windows)

`uv pip install -r requirements.txt`

`sh 00-setup.sh`

`python -m ipykernel install --user --name=.venv --display-name="str_tutorial"`


(나 참고용)
jupyter kernel 삭제하려면

```
jupyter kernelspec list
jupyter kernelspec uninstall 커널이름
```