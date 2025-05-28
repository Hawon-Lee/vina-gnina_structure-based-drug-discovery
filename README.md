
## UV environment 구ㅅㅇ하기


```bash
pip install uv
uv venv venv --python=3.9.19
```
---
Activate virtual environment

**Linux / macOS** `source venv/bin/activate` 

**Windows** `venv\Scripts\activate`

----
venv 외에 활성화된 가상환경이 있다면 전부 비활성화합니다.

**Conda** `conda deactivate`

**기타 가상환경** `deactivate`

---
다음 명령어로 requirements 를 모두 설치합니다.

`uv pip install -r requirements.txt`

다음 명령어는 docking tool들을 설치합니다 (autodock-vina, gnina)

`sh 00-docking_install.sh`

현재 가상환경을 jupyter kernel 에 등록합니다.

`python -m ipykernel install --user --name=venv --display-name="str_tutorial"`

----------------------------------------------------------------------------
(참고용)
등록된 jupyter kernel 을 삭제하려면...

```
jupyter kernelspec list
jupyter kernelspec uninstall 커널이름
```