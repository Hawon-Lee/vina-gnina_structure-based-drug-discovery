
우선 모든 가상환경 deactivate하기

## UV environment 구성
`pip install uv`

`uv venv --python=3.9.19`

`source .venv/bin/activate` (Linux/macOS) / `.venv\Scripts\activate` (Windows)

.venv 외에 활성화된 가상환경이 있다면 전부 비활성화합니다.

`conda deactivate` or `deactivate`

다음 명령어로 requirements 를 모두 설치합니다.

`uv pip install -r requirements.txt`

다음 명령어는 docking tool들을 설치합니다 (autodock-vina, gnina)

`sh 00-docking_install.sh`

`python -m ipykernel install --user --name=.venv --display-name="str_tutorial"`

------------------------------------------------------------------------------


(참고용)
등록된 jupyter kernel 삭제하려면...

```
jupyter kernelspec list
jupyter kernelspec uninstall 커널이름
```